CREATE TABLE "food" (
    "id" INTEGER,
    "name" TEXT NOT NULL, 
    "portion" REAL NOT NULL,
    "calories" REAL NOT NULL,
    "fat" REAL NOT NULL,
    "carbs" REAL NOT NULL,
    "protein" REAL NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE "person_idni" (
    "id" INTEGER,
    "insert_date" TEXT NOT NULL,
    "calories" REAL NOT NULL,
    "fat" REAL NOT NULL,
    "carbs" REAL NOT NULL,
    "protein" REAL NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE "diary" (
    "id" INTEGER,
    "date" TEXT NOT NULL,
    "total_calories_consumed" REAL NOT NULL DEFAULT 0,
    "total_fat_consumed" REAL NOT NULL DEFAULT 0,
    "total_carbs_consumed" REAL NOT NULL DEFAULT 0,
    "total_protein_consumed" REAL NOT NULL DEFAULT 0,
    PRIMARY KEY("id")
);

CREATE TABLE "food_consumed" (
    "id" INTEGER,
    "date" TEXT NOT NULL,
    "food_name" TEXT NOT NULL,
    "portion_consumed" REAL NOT NULL,
    "calories" REAL NOT NULL,
    "fat" REAL NOT NULL,
    "carbs" REAL NOT NULL,
    "protein" REAL NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("food_name") REFERENCES "food"("name") 
);

CREATE TABLE "weight" (
"date" DATE,
"weight" REAL NOT NULL,
PRIMARY KEY("date")
);
