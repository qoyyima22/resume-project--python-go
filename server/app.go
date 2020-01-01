package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"time"

	_ "github.com/lib/pq"
	"github.com/mitchellh/mapstructure"
)

const (
	// host = "36.86.63.182"
	host              = `127.0.0.1`
	port              = 5432
	user              = `postgres`
	password          = `Mantap123`
	dbname            = `cv-data`
	listen_addresses  = `*`
	binary_parameters = `yes`
)

type sections_content struct {
	Section_work_experience_en string `json:"section_work_experience_en"`
	Section_work_experience_id string `json:"section_work_experience_id"`
	Section_educations_en      string `json:"section_educations_en"`
	Section_educations_id      string `json:"section_educations_id"`
	Section_skills_en          string `json:"section_skills_en"`
	Section_skills_id          string `json:"section_skills_id"`
	Section_summary_en         string `json:"section_summary_en"`
	Section_summary_id         string `json:"section_summary_id"`
	Section_interests_en       string `json:"section_interests_en"`
	Section_interests_id       string `json:"section_interests_id"`
	Section_extras_en          string `json:"section_extras_en"`
	Section_extras_id          string `json:"section_extras_id"`
	Section_languages_en       string `json:"section_languages_en"`
	Section_languages_id       string `json:"section_languages_id"`
	Section_title_en           string `json:"section_title_en"`
	Section_title_id           string `json:"section_title_id"`
	Section_affiliations_en    string `json:"section_affiliations_en"`
	Section_affiliations_id    string `json:"section_affiliations_id"`
	Section_certifications_en  string `json:"section_certifications_en"`
	Section_certifications_id  string `json:"section_certifications_id"`
	Section_awards_en          string `json:"section_awards_en"`
	Section_awards_id          string `json:"section_awards_id"`
}

type req_body struct {
	Folder            string
	HTML              string
	Title             string
	En                string
	Id                string
	Score             int
	Sections          []string
	SectionsId        []string
	SectionCategory   []string
	SectionCategoryId []string
	SectionsContent   map[string]interface{}
}

func main() {
	handler := http.NewServeMux()
	handler.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Halo bro"))
	})
	// if err := http.ListenAndServe(":8080", nil); err != nil {
	// 	panic(err)
	// }
	handler.HandleFunc("/insert/cv", processRequest)
	if err := http.ListenAndServe(":8080", handler); err != nil {
		panic(err)
	}
}

func processRequest(w http.ResponseWriter, r *http.Request) {
	decoder := json.NewDecoder(r.Body)
	var t req_body
	err := decoder.Decode(&t)
	if err != nil {
		log.Println("error: ", err)
	}

	var nsc sections_content

	mapstructure.Decode(t.SectionsContent, &nsc)

	w.Write([]byte("Success "))
	insertToTable(t.Folder, t.Title, t.HTML, t.En, t.Id, t.Score, nsc, t.Sections, t.SectionsId, t.SectionCategory, t.SectionCategoryId)
}

func insertToTable(Folder string, Title string, HTML string, En string, Id string, Score int, nsc sections_content, Sections []string, SectionsId []string, SectionCategory []string, SectionCategoryId []string) {

	// fmt.Println("\n=======\n", nsc, "\n============\n", nsc.Section_title_en, "NINININIG")

	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}

	defer db.Close()

	sqlStatement := `
	INSERT INTO cvs (
		id,
		created_at,
		title,
		html,
		cv_en,
		cv_id,
		score,
		folder,
		work_experience_en,
		work_experience_id,
		educations_en,
		educations_id,
		skills_en,
		skills_id,
		summary_en,
		summary_id,
		interests_en,
		interests_id,
		extras_en,
		extras_id,
		languages_en,
		languages_id,
		title_en,
		title_id,
		affiliations_en,
		affiliations_id,
		certifications_en,
		certifications_id,
		awards_en,
		awards_id,
		sections,
		sections_id,
		sections_category,
		sections_category_id
	)
	VALUES (
		$1,
		$2,
		$3,
		$4,
		$5,
		$6,
		$7,
		$8,
		$9,
		$10,
		$11,
		$12,
		$13,
		$14,
		$15,
		$16,
		$17,
		$18,
		$19,
		$20,
		$21,
		$22,
		$23,
		$24,
		$25,
		$26,
		$27,
		$28,
		$29,
		$30,
		$31,
		$32,
		$33,
		$34
	)
    RETURNING id
	`
	id := getLastId() + 1
	err = db.QueryRow(
		sqlStatement,
		id,
		time.Now(),
		Title,
		HTML,
		En,
		Id,
		Score,
		Folder,
		nsc.Section_work_experience_en,
		nsc.Section_work_experience_id,
		nsc.Section_educations_en,
		nsc.Section_educations_id,
		nsc.Section_skills_en,
		nsc.Section_skills_id,
		nsc.Section_summary_en,
		nsc.Section_summary_id,
		nsc.Section_interests_en,
		nsc.Section_interests_id,
		nsc.Section_extras_en,
		nsc.Section_extras_id,
		nsc.Section_languages_en,
		nsc.Section_languages_id,
		nsc.Section_title_en,
		nsc.Section_title_id,
		nsc.Section_affiliations_en,
		nsc.Section_affiliations_id,
		nsc.Section_certifications_en,
		nsc.Section_certifications_id,
		nsc.Section_awards_en,
		nsc.Section_awards_id,
		strings.Join(Sections, ", "),
		strings.Join(SectionsId, ", "),
		strings.Join(SectionCategory, ", "),
		strings.Join(SectionCategoryId, ", "),
	).
		Scan(&id)
	if err != nil {
		panic(err)
	}

	fmt.Println("new record ID is:", id)
}

func getLastId() int {
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}

	defer db.Close()

	sqlStatement := `
	SELECT id
	FROM cvs
	ORDER BY id DESC
	LIMIT 1
	`

	rows, err := db.Query(sqlStatement)
	if err != nil {
		log.Fatal("Error:", err)
	}
	defer rows.Close()
	var id int
	for rows.Next() {
		if err := rows.Scan(&id); err != nil {
			log.Fatal(err)
		}
		fmt.Println(id)
	}
	if err := rows.Err(); err != nil {
		log.Fatal(err)
	}
	return id
}
