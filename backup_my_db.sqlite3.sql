BEGIN TRANSACTION;
CREATE TABLE "cat" (
	"id"	INTEGER NOT NULL,
	"name"	NVCHAR(80) NOT NULL,
	"owner_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("owner_id") REFERENCES "person"("id") ON DELETE CASCADE
);
INSERT INTO "cat" VALUES(1,'Chat',1);
INSERT INTO "cat" VALUES(2,'boule de neige',1);
CREATE TABLE "person" (
	"id"	INTEGER NOT NULL,
	"name"	NVARCHAR(80) NOT NULL,
	"age"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "person" VALUES(1,'Irina',35);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('person',1);
INSERT INTO "sqlite_sequence" VALUES('cat',2);
COMMIT;
