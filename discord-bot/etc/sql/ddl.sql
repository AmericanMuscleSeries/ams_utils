create table driver (
    discord_id int  unique  not null,
    iracing_id int  unique  not null,
    pref_name varchar(255),
    team varchar(255),
    location varchar(255),
    number varchar(3),
    primary key (discord_id)
);

create table season (
    id int  not null  auto_increment,
    season_number int  not null,
    start_date  date,
    primary key (id)
);

create table registration (
    id int  not null  auto_increment,
    season int  not null,
    driver int  not null,
    registered_at timestamp  default current_timestamp,
    division varchar(3),
    primary key (id),
    foreign key (season) references season(id),
    foreign key (driver) references driver(discord_id)
);

create table race (
    id int  not null  auto_increment,
    season int  not null,
    round_num int  not null,
    race_date date  not null,
    track varchar(255),
    primary key (id),
    foreign key (season) references season(id)
);
