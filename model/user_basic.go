package model

import (
	"gorm.io/gorm"
)

type UserBasic struct {
	gorm.Model
	Phone    string
	Password string `json:"password,omitempty"`
}

// var DB *gorm.DB

func (table *UserBasic) TableName() string {
	return "user_basic"
}

func CreateUser(user *UserBasic) error {
	migrator := DB.Migrator()
	exist := migrator.HasTable("user_basic")
	if !exist {
		migrator.AutoMigrate(&user)
	}
	return DB.Create(&user).Error
}

func FindUserByPhone(phone string) UserBasic {
	user := UserBasic{}
	DB.Where("phone = ?", phone).First(&user)
	return user
}

func CheckUserExist(phone string) bool {
	var user UserBasic

	DB.Where("phone = ?", user.Phone).First(&user)
	return user.Phone != ""
}