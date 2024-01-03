package model

import (
	"ai-bot/utils"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/spf13/viper"
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
	DB, error := gorm.Open(mysql.Open(dns), &gorm.Config{Logger: newLogger})
	// directly exit if database open error
	if error != nil {
		os.Exit(1)
	}

	fmt.Println("MySQL inited.", viper.GetString("mysql"))

	// auto create the tables
	DB.AutoMigrate(
		UserBasic{},
		// messages are stored in vector db now 
		// Message{}, 
		RolePrompt{},
	)
}
