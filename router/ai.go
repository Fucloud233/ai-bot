package router

import (
	"ai-bot/service"
	"github.com/gin-gonic/gin"
)

func Router() *gin.Engine {
	r := gin.Default()
	r.GET("index/login", service.Login)
	return r
}
