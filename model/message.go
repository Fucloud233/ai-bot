package model

import "time"

type Message struct {
	Phone string `json:"-" `
	Role string `json:"role"`
	BotRole string `json:"-"`
	Time time.Time `json:"time"`
	Content string `json:"content"`
}

func AddMessages(messages *[]Message) error {
	return DB.Create(&messages).Error
}

func GetNewestMessage(phone string, n int) ([]Message, error) {
	var message []Message
	err := DB.Order("time desc").Limit(n).Where("phone = ?", phone).Find(&message).Error
	// reserve array
	for i, j := 0, len(message)-1; i < j; i, j = i+1, j-1 {
		message[i], message[j] = message[j], message[i]
	}
	return message, err
} 