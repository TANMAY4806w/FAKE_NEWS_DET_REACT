import React from 'react';
import { motion } from 'framer-motion';

export default function About() {
  return (
    <section className="flex justify-center mt-24 px-4 fade-in">
      <div className="w-full max-w-4xl glass-panel p-8 md:p-12 text-center relative z-10 animate-fadeIn">

        {/* ===== Hero Section ===== */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        >
          <h1 className="text-4xl md:text-5xl font-extrabold mb-6 text-gradient tracking-tight drop-shadow-sm">
            About the Project
          </h1>

          <p className="text-gray-300 font-light text-lg mb-8 max-w-2xl mx-auto leading-relaxed">
            The <span className="text-primary font-semibold">Fake News Detector</span> is an AI-driven platform
            that combines <span className="text-secondary font-semibold">Machine Learning</span> and
            <span className="text-secondary font-semibold"> Web Verification</span> to detect and prevent
            misinformation across digital platforms.
          </p>
        </motion.div>

        {/* ===== How It Works Section ===== */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className="bg-[#0B0F19]/50 border border-white/5 shadow-inner rounded-xl p-8 text-left backdrop-blur-sm"
        >
          <h2 className="text-2xl font-semibold text-primary mb-4 flex items-center gap-2">
            ⚙️ How It Works
          </h2>

          <p className="text-gray-300 leading-relaxed mb-5 font-light">
            The system uses a <span className="text-secondary font-semibold">hybrid approach</span> that integrates
            machine learning with online verification for optimal accuracy:
          </p>

          <motion.ul
            className="list-disc list-inside text-gray-300 space-y-3 pl-3 font-light"
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
              🧮 A <span className="text-primary font-semibold">Logistic Regression</span> model trained with
              <span className="text-secondary font-semibold"> TF-IDF vectorization</span> analyzes linguistic patterns
              in the text.
            </motion.li>

            <motion.li variants={{ hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0 } }}>
              🌐 A <span className="text-primary font-semibold">Web Verification Engine</span> performs real-time
              searches to compare facts with credible online sources.
            </motion.li>

            <motion.li variants={{ hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0 } }}>
              📊 Combined results generate a <span className="text-accent font-semibold">credibility score</span>,
              showing whether the news is likely <span className="text-danger font-semibold glow-fake px-1 rounded bg-[#1A0B0B]">fake</span> or
              <span className="text-accent font-semibold glow-real px-1 rounded bg-[#0B1A14]"> true</span>.
            </motion.li>
          </motion.ul>
        </motion.div>

        {/* ===== Technologies Used ===== */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2, ease: 'easeOut' }}
          className="mt-10 bg-[#0B0F19]/50 border border-white/5 rounded-xl shadow-inner p-8 backdrop-blur-sm"
        >
          <h2 className="text-2xl font-semibold text-primary mb-6 flex items-center justify-center gap-2">
            🧩 Technologies Used
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 text-center">
            <motion.div whileHover={{ scale: 1.05 }} className="flex flex-col items-center">
              <span className="text-4xl drop-shadow-[0_0_8px_rgba(59,130,246,0.5)]">🤖</span>
              <span className="mt-3 text-gray-300 font-medium tracking-wide">Machine Learning</span>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} className="flex flex-col items-center">
              <span className="text-4xl drop-shadow-[0_0_8px_rgba(139,92,246,0.5)]">🔤</span>
              <span className="mt-3 text-gray-300 font-medium tracking-wide">TF-IDF</span>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} className="flex flex-col items-center">
              <span className="text-4xl drop-shadow-[0_0_8px_rgba(16,185,129,0.5)]">🌍</span>
              <span className="mt-3 text-gray-300 font-medium tracking-wide">Web Scraper</span>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} className="flex flex-col items-center">
              <span className="text-4xl drop-shadow-[0_0_8px_rgba(59,130,246,0.5)]">⚛️</span>
              <span className="mt-3 text-gray-300 font-medium tracking-wide">React</span>
            </motion.div>
          </div>
        </motion.div>

        {/* ===== Purpose Box ===== */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3, ease: 'easeOut' }}
          className="mt-10 p-6 bg-[#0B1220]/80 border border-primary/50 shadow-glowBlue rounded-lg backdrop-blur-sm"
        >
          <p className="text-white text-lg leading-relaxed font-light">
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
