package model

import (
	"ai-bot/utils"
	"fmt"
	"log"
	"os"
	"time"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

var DB *gorm.DB


func InitMySQL() {
	newLogger := logger.New(
		log.New(os.Stdout, "\r\n", log.LstdFlags),
		logger.Config{
			SlowThreshold: time.Second,
			LogLevel:      logger.Info,
			Colorful:      true,
		},
	)

	dns := utils.DatabaseConfig.ToDNS();
	
	var err error
	DB, err = gorm.Open(mysql.Open(dns), &gorm.Config{Logger: newLogger})
	// directly exit if database open error
	if err != nil {
		fmt.Println("MySQL连接错误")
		os.Exit(1)
	}

	// auto create the tables
	DB.AutoMigrate(
		UserBasic{},
		// messages are stored in vector db now 
		// Message{}, 
		RolePrompt{},
	)
}
