package main

import (
	"ai-bot/router"
	"ai-bot/utils"
)

func main() {
	utils.InitConfig()
	utils.InitMySQL()
	r := router.Router()

	r.Run(":6062")
}
