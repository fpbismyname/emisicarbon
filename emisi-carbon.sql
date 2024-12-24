-- Membuat database emisicarbon
CREATE DATABASE emisicarbon;
USE emisicarbon;

-- Tabel users: Menyimpan informasi pengguna atau perusahaan
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'company', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel sources: Menyimpan jenis sumber emisi, seperti transportasi, listrik, dan industri
CREATE TABLE sources (
    source_id INT PRIMARY KEY AUTO_INCREMENT,
    source_name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel emissions: Menyimpan data emisi yang dilaporkan
CREATE TABLE emissions (
    emission_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    source_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,        -- Jumlah emisi dalam metrik ton
    emission_date DATE NOT NULL,           -- Tanggal emisi terjadi
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Tanggal dilaporkan
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE SET NULL
);

-- Tabel carbon_factors: Menyimpan faktor konversi untuk menghitung emisi berdasarkan aktivitas tertentu
CREATE TABLE carbon_factors (
    factor_id INT PRIMARY KEY AUTO_INCREMENT,
    source_id INT NOT NULL,
    description TEXT,
    conversion_factor DECIMAL(10, 4) NOT NULL, -- Nilai konversi untuk menghitung emisi (kg CO2 per unit aktivitas)
    unit VARCHAR(20) NOT NULL,                 -- Unit aktivitas, misalnya 'kWh' atau 'liter'
    FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE SET NULL
);

-- Tabel activities: Menyimpan aktivitas pengguna yang memicu emisi, dengan referensi ke faktor karbon untuk konversi
CREATE TABLE activities (
    activity_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    factor_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,  -- Jumlah unit aktivitas (misalnya kWh listrik, liter bensin)
    activity_date DATE NOT NULL,     -- Tanggal aktivitas terjadi
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (factor_id) REFERENCES carbon_factors(factor_id) ON DELETE SET NULL
);

-- Tabel reports: Menyimpan laporan bulanan atau tahunan dari data emisi
CREATE TABLE reports (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_emission DECIMAL(12, 2) NOT NULL,    -- Total emisi dalam periode ini
    report_generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Tabel offsets: Menyimpan informasi tentang inisiatif offset karbon, seperti penanaman pohon atau investasi energi terbarukan
CREATE TABLE offsets (
    offset_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    project_name VARCHAR(100) NOT NULL,
    offset_amount DECIMAL(10, 2) NOT NULL,     -- Jumlah emisi yang di-offset dalam metrik ton
    offset_date DATE NOT NULL,                 -- Tanggal offset
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Tabel goals: Menyimpan target pengurangan emisi untuk pengguna atau perusahaan
CREATE TABLE goals (
    goal_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    target_emission DECIMAL(10, 2) NOT NULL,   -- Target emisi yang ingin dicapai
    deadline DATE NOT NULL,                    -- Tenggat waktu untuk mencapai target
    status ENUM('in_progress', 'achieved', 'missed') DEFAULT 'in_progress',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Tabel selesai dibuat