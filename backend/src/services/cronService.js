const cron = require('node-cron');
const moment = require('moment-timezone');
const { db } = require('../db/firebase');
const { sendEmail, emailTemplates } = require('./emailService');

const startCronJobs = () => {
  console.log('⏳ Starting background cron jobs...');

  // Run every minute
  cron.schedule('* * * * *', async () => {
    try {
      const now = moment.utc();

      // ─── 1. HANDLE 20-MINUTE SLOT EXPIRY ───
      // Find appointments created > 20 mins ago that are NOT confirmed
      const expiryThreshold = now.clone().subtract(20, 'minutes').toISOString();

      // Optimization: Fetch all 'scheduled' appointments once per minute and filter in JS
      // This avoids ALL Firestore composite index requirements (which occur when combining status == X with a range).
      const scheduledSnapshot = await db.collection('appointments')
        .where('status', '==', 'scheduled')
        .get();

      const scheduledDocs = scheduledSnapshot.docs;

      // ─── 1. HANDLE 20-MINUTE SLOT EXPIRY ───
      for (const doc of scheduledDocs) {
        const appt = doc.data();
        
        // Filter in JS instead of Firestore
        const isExpiredInTime = appt.created_at <= expiryThreshold;
        if (!isExpiredInTime || appt.is_confirmed || appt.status === 'expired') continue;

        console.log(`🕒 Terminating expired slot: ${appt.id}`);
        await db.collection('appointments').doc(doc.id).update({
          status: 'expired',
          updated_at: new Date().toISOString()
        });
        await db.collection('patient_queue').doc(doc.id).delete();

        const pDoc = await db.collection('users').doc(appt.patient_id).get();
        const dDoc = await db.collection('users').doc(appt.doctor_id).get();

        if (pDoc.exists) {
          const patient = pDoc.data();
          const doctorName = dDoc.exists ? dDoc.data().full_name : 'your doctor';
          const rescheduleLink = `${process.env.FRONTEND_URL}/patient/book-opd?doctor_id=${appt.doctor_id}`;
          const template = emailTemplates.appointmentExpired(patient.full_name, doctorName, appt.appointment_time, rescheduleLink);
          const emailRes = await sendEmail({ to: patient.email, subject: template.subject, html: template.html });
          await db.collection('appointments').doc(doc.id).update({
            expiry_email_sent: emailRes.success,
            expiry_email_logged_at: new Date().toISOString()
          });
        }
      }

      // ─── 2. HANDLE 20-MINUTE START REMINDER ───
      const targetMin = now.clone().add(20, 'minutes').toISOString();
      const targetMax = now.clone().add(21, 'minutes').toISOString();

      for (const doc of scheduledDocs) {
        const appt = doc.data();
        
        // Filter in JS instead of Firestore
        const isWithinWindow = appt.start_time_utc >= targetMin && appt.start_time_utc < targetMax;
        if (!isWithinWindow || appt.reminder_sent || appt.status === 'expired') continue;

        const ppDoc = await db.collection('users').doc(appt.patient_id).get();
        const dpDoc = await db.collection('users').doc(appt.doctor_id).get();

        if (ppDoc.exists && dpDoc.exists) {
          const patient = ppDoc.data();
          const doctor = dpDoc.data();
          const template = emailTemplates.appointmentReminder(patient.full_name, doctor.full_name, appt.appointment_date, appt.start_time_utc);
          sendEmail({ to: patient.email, subject: template.subject, html: template.html });
          await db.collection('appointments').doc(doc.id).update({ reminder_sent: true });
        }
      }

      // ─── 3. HANDLE 1-HOUR REMINDER ───
      const hourStart = now.clone().add(55, 'minutes').toISOString();
      const hourEnd = now.clone().add(65, 'minutes').toISOString();

      for (const doc of scheduledDocs) {
        const appt = doc.data();

        // Filter in JS instead of Firestore
        const isWithinHour = appt.start_time_utc >= hourStart && appt.start_time_utc <= hourEnd;
        if (!isWithinHour || appt.reminder_1h_sent || appt.status === 'expired') continue;

        const ppDoc = await db.collection('users').doc(appt.patient_id).get();
        const dpDoc = await db.collection('users').doc(appt.doctor_id).get();

        if (ppDoc.exists && dpDoc.exists) {
          const patient = ppDoc.data();
          const doctor = dpDoc.data();
          const template = emailTemplates.reminder1Hour(patient.full_name, doctor.full_name, appt.appointment_date, appt.appointment_time);
          await sendEmail({ to: patient.email, subject: template.subject, html: template.html });
          await db.collection('appointments').doc(doc.id).update({ reminder_1h_sent: true });
          console.log(`⏰ 1-hour reminder sent to ${patient.email} for appt ${appt.id}`);
        }
      }
    } catch (error) {
      console.error('❌ Cron Job Error:', error);
    }
  });
};

module.exports = { startCronJobs };
