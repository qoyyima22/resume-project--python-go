package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	_ "github.com/lib/pq"
)

const (
	host     = "127.0.0.1"
	port     = 5432
	user     = "postgres"
	password = "Mantap123"
	dbname   = "cv-data"
)

type req_body struct {
	Folder string
	HTML   string
	Title  string
	En     string
	Id     string
	Score  int
}

func main() {
	http.HandleFunc("/insert/cv", processRequest)
	if err := http.ListenAndServe(":8080", nil); err != nil {
		panic(err)
	}
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Halo bro"))
	})
	if err := http.ListenAndServe(":8080", nil); err != nil {
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
	println(t.Score)

	w.Write([]byte("Success "))
	insertToTable(t.Folder, t.Title, t.HTML, t.En, t.Id, t.Score)
}

func insertToTable(Folder string, Title string, HTML string, En string, Id string, Score int) {
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}

	defer db.Close()

	sqlStatement := `
    INSERT INTO cvs (id, created_at, title, html, cv_en, cv_id, score, folder)
    VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
    RETURNING id
	`
	id := getLastId() + 1
	err = db.QueryRow(sqlStatement, id, time.Now(), Title, HTML, En, Id, Score, Folder).
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
