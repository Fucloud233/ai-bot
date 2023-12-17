package service

import (
	"ai-bot/model"
	"github.com/gin-gonic/gin"
	"net/http"
)

//func CreateUser(c *gin.Context) {
//	user := model.UserBasic{}
//	user.Phone = c.Query("phone")
//	user.Password = c.Query("password")
//	err := model.CreateUser(&user)
//	if err != nil {
//		c.JSON(http.StatusInternalServerError, gin.H{})
//	} else {
//		c.JSON(http.StatusOK, gin.H{})
//	}
//}

func Login(c *gin.Context) {
	user := model.UserBasic{}
	phone := c.Query("phone")
	password := c.Query("phone")
	findUser := model.FindUserByPhone(phone)
	if findUser.Phone != "" {
		if password == findUser.Password {
			c.JSON(http.StatusOK, gin.H{})
		} else {
			c.JSON(http.StatusOK, gin.H{
				"message": "密码错误",
			})
			return
		}
	} else {
		user.Phone = phone
		user.Password = password
		err := model.CreateUser(&user)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{})
		} else {
			c.JSON(http.StatusOK, gin.H{})
		}
	}
}
