package router

import (
	"example.com/m/v2/service"
	"github.com/gin-gonic/gin"
)

func Router() *gin.Engine {
	gin.SetMode(gin.DebugMode)

	r := gin.Default()
	r.GET("index/login", service.Login)
	r.POST("user", service.CreateUser)


	r.POST("messages", service.PostMessages)

	return r
}
