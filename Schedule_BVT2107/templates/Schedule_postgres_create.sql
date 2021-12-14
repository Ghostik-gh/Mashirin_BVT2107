CREATE TABLE "public.subject" (
	"id" serial NOT NULL,
	"subject_name" varchar(50) NOT NULL,
	CONSTRAINT "subject_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.timetable" (
	"id" serial NOT NULL,
	"day" int NOT NULL,
	"top_week" bool NOT NULL,
	"fk_subject" int NOT NULL,
	"room" int NOT NULL,
	"start_time" varchar(20) NOT NULL,
	CONSTRAINT "timetable_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.teachers" (
	"id" serial NOT NULL,
	"full_name" varchar(50) NOT NULL,
	"fk_subject" int NOT NULL,
	CONSTRAINT "teachers_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);




ALTER TABLE "timetable" ADD CONSTRAINT "timetable_fk0" FOREIGN KEY ("fk_subject") REFERENCES "subject"("id");

ALTER TABLE "teachers" ADD CONSTRAINT "teachers_fk0" FOREIGN KEY ("fk_subject") REFERENCES "subject"("id");




