import React from 'react';
import { motion } from 'framer-motion';

export default function About() {
  return (
    <section className="flex justify-center mt-24 px-4 fade-in">
      <div className="w-full max-w-4xl bg-white shadow-lg rounded-2xl p-8 md:p-12 border border-blue-100 text-center">

        {/* ===== Hero Section ===== */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        >
          <h1 className="text-4xl md:text-5xl font-extrabold mb-4 bg-gradient-to-r from-primary to-secondary text-transparent bg-clip-text">
            About the Project
          </h1>

          <p className="text-gray-600 text-lg mb-8 max-w-2xl mx-auto">
            The <span className="text-primary font-semibold">Fake News Detector</span> is an AI-driven platform
            that combines <span className="text-secondary font-medium">Machine Learning</span> and
            <span className="text-secondary font-medium"> Web Verification</span> to detect and prevent
            misinformation across digital platforms.
          </p>
        </motion.div>

        {/* ===== How It Works Section ===== */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className="bg-gradient-to-br from-blue-50 to-cyan-50 border border-blue-100 rounded-xl shadow-md p-8 text-left"
        >
          <h2 className="text-2xl font-semibold text-primary mb-4 flex items-center gap-2">
            ⚙️ How It Works
          </h2>

          <p className="text-gray-700 leading-relaxed mb-5">
            The system uses a <span className="text-secondary font-medium">hybrid approach</span> that integrates
            machine learning with online verification for optimal accuracy:
          </p>

          <motion.ul
            className="list-disc list-inside text-gray-700 space-y-3 pl-3"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={{
              hidden: { opacity: 0, y: 10 },
              visible: {
                opacity: 1,
                y: 0,
                transition: {
                  staggerChildren: 0.15,
                  duration: 0.4,
                  ease: 'easeOut',
                },
              },
            }}
          >
            <motion.li variants={{ hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0 } }}>
              🧮 A <span className="text-primary font-medium">Logistic Regression</span> model trained with
              <span className="text-secondary font-medium"> TF-IDF vectorization</span> analyzes linguistic patterns
              in the text.
            </motion.li>

            <motion.li variants={{ hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0 } }}>
              🌐 A <span className="text-primary font-medium">Web Verification Engine</span> performs real-time
              searches to compare facts with credible online sources.
            </motion.li>

            <motion.li variants={{ hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0 } }}>
              📊 Combined results generate a <span className="text-accent font-semibold">credibility score</span>,
              showing whether the news is likely <span className="text-red-600 font-semibold">fake</span> or
              <span className="text-green-600 font-semibold"> true</span>.
            </motion.li>
          </motion.ul>
        </motion.div>

        {/* ===== Technologies Used ===== */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2, ease: 'easeOut' }}
          className="mt-10 bg-white border border-gray-100 rounded-xl shadow-md p-8"
        >
          <h2 className="text-2xl font-semibold text-primary mb-4 flex items-center gap-2">
            🧩 Technologies Used
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 text-center">
            <motion.div whileHover={{ scale: 1.05 }} className="flex flex-col items-center">
              <span className="text-3xl">🤖</span>
              <span className="mt-2 text-gray-700 font-medium">Machine Learning</span>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} className="flex flex-col items-center">
              <span className="text-3xl">🔤</span>
              <span className="mt-2 text-gray-700 font-medium">TF-IDF</span>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} className="flex flex-col items-center">
              <span className="text-3xl">🌍</span>
              <span className="mt-2 text-gray-700 font-medium">Web Scraper</span>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} className="flex flex-col items-center">
              <span className="text-3xl">⚛️</span>
              <span className="mt-2 text-gray-700 font-medium">React</span>
            </motion.div>
          </div>
        </motion.div>

        {/* ===== Purpose Box ===== */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3, ease: 'easeOut' }}
          className="mt-10 p-6 bg-gradient-to-r from-blue-100 to-cyan-100 border border-blue-200 rounded-lg shadow-sm"
        >
          <p className="text-gray-800 text-lg leading-relaxed">
            💡 The <span className="font-semibold text-primary">goal</span> of this project is to enhance
            <span className="text-secondary font-semibold"> digital literacy</span> and promote the
            <span className="font-semibold text-primary"> responsible sharing</span> of information online.
            Through AI-powered analysis, users can quickly identify the credibility of news content and help
            build a more informed society.
          </p>
        </motion.div>
      </div>
    </section>
  );
}
