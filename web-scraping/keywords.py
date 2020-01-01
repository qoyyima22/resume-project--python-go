
def keywordFunc():
    keywords = {}
    keywords["section_work_experience_en"] = [
        "EXPERIENCE",
        "EXPERIENCES",
        "WORK",
        "WORK EXPERIENCE",
        "WORK EXPERIENCES",
        "EXPERIENCE WORK",
        "EXPERIENCES WORK",
        "WORK HISTORY"
    ]

    keywords["section_work_experience_id"] = [
        "PENGALAMAN",
        "KERJA",
        "PENGALAMAN KERJA",
        "PENGALAMAN BEKERJA",
        "RIWAYAT PEKERJAAN"
    ]

    keywords["section_educations_en"] = [
        "EDUCATION",
        "EDUCATIONAL EXPERIENCE",
        "FORMAL EDUCATION",
        "NON-FORMAL EDUCATION",
        "NONFORMAL EDUCATION",
        "INFORMAL EDUCATION",
        "EDUCATION AND TRAINING"
    ]

    keywords["section_educations_id"] = [
        "PENDIDIKAN",
        "PENGALAMAN PENDIDIKAN",
        "PENDIDIKAN FORMAL",
        "PENDIDIKAN NON-FORMAL",
        "PENDIDIKAN NONFORMAL",
        "PENDIDIKAN INFORMAL",
        "PENDIDIKAN DAN PELATIHAN"
    ]

    keywords["section_skills_en"] = [
        "SKILLS"
    ]

    keywords["section_skills_id"] = [
        "KEMAMPUAN",
        "SKILLS",
        "SKILL"
    ]

    keywords["section_summary_en"] = [
        "SUMMARY",
        "ABOUT ME"
    ]

    keywords["section_summary_id"] = [
        "RINGKASAN DIRI",
        "TENTANG SAYA",
        "RINGKASAN"
    ]

    keywords["section_interests_en"] = [
        "INTERESTS"
    ]

    keywords["section_interests_id"] = [
        "KEINGINTAHUAN"
    ]

    keywords["section_extras_en"] = [
        "VOLUNTEER",
        "VOLUNTEER WORK",
        "ORGANIZATIONAL EXPERIENCE",
        "VOLUNTEER EXPERIENCE",
        "VOLUNTEER WORK EXPERIENCE",
        "ORGANIZATIONAL",
        "ORGANIZATION"
    ]

    keywords["section_extras_id"] = [
        "SUKARELA",
        "KERJA SUKARELA",
        "PENGALAMAN KERJA SUKARELA",
        "ORGANISASI",
        "PENGALAMAN ORGANISASI",
        "PENGALAMAN BERORGANISASI"
    ]

    keywords["section_languages_en"] = [
        "LANGUAGES",
        "LANGUAGE",
        "LANGUAGES PROFICIENCY",
        "LANGUAGE PROFICIENCY"
    ]

    keywords["section_languages_id"] = [
        "BAHASA",
        "KEMAMPUAN BAHASA",
        "KEAHLIAN BAHASA"
    ]

    keywords["section_title_en"] = [
        "TITLE"
    ]

    keywords["section_title_id"] = [
        "JUDUL"
    ]

    keywords["section_affiliations_en"] = [
        "AFFILIATIONS",
        "AFFILIATION",
        "REFERENCES",
        "REFERENCE"
    ]

    keywords["section_affiliations_id"] = [
        "AFILIASI",
        "REFERENSI"
    ]

    keywords["section_certifications_en"] = [
        "CERTIFICATION",
        "CERTIFICATIONS"
    ]

    keywords["section_certifications_id"] = [
        "SERTIFIKASI"
    ]

    keywords["section_awards_en"] = [
        "AWARDS"
    ]

    keywords["section_awards_id"] = [
        "PENGHARGAAN"
    ]

    return keywords


class Sections:
    def __init__(self, section_work_experience_en="",
                 section_work_experience_id="",
                 section_educations_en="",
                 section_educations_id="",
                 section_skills_en="",
                 section_skills_id="",
                 section_summary_en="",
                 section_summary_id="",
                 section_interests_en="",
                 section_interests_id="",
                 section_extras_en="",
                 section_extras_id="",
                 section_languages_en="",
                 section_languages_id="",
                 section_title_en="",
                 section_title_id="",
                 section_affiliations_en="",
                 section_affiliations_id="",
                 section_certifications_en="",
                 section_certifications_id="",
                 section_awards_en="",
                 section_awards_id=""):
        self.section_work_experience_en = section_work_experience_en
        self.section_work_experience_id = section_work_experience_id
        self.section_educations_en = section_educations_en
        self.section_educations_id = section_educations_id
        self.section_skills_en = section_skills_en
        self.section_skills_id = section_skills_id
        self.section_summary_en = section_summary_en
        self.section_summary_id = section_summary_id
        self.section_interests_en = section_interests_en
        self.section_interests_id = section_interests_id
        self.section_extras_en = section_extras_en
        self.section_extras_id = section_extras_id
        self.section_languages_en = section_languages_en
        self.section_languages_id = section_languages_id
        self.section_title_en = section_title_en
        self.section_title_id = section_title_id
        self.section_affiliations_en = section_affiliations_en
        self.section_affiliations_id = section_affiliations_id
        self.section_certifications_en = section_certifications_en
        self.section_certifications_id = section_certifications_id
        self.section_awards_en = section_awards_en
        self.section_awards_id = section_awards_id

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value
