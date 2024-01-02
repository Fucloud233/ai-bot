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
	DB, _ = gorm.Open(mysql.Open(utils.DatabaseConfig.ToDNS()),
		&gorm.Config{Logger: newLogger})

	fmt.Println("MySQL inited.", viper.GetString("mysql"))

	// auto create the tables
	DB.AutoMigrate(
		UserBasic{},
		// messages are stored in vector db now 
		// Message{}, 
		RolePrompt{},
	)
}
