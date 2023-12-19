package model

import "time"

const (
	User string = "user"
	Assistant string = "assistant"
)

type Message struct {
	Phone string `json:"-" `
	BotRole string `json:"-"`
	Time time.Time `json:"time"`
	SimpleMessage
}

type SimpleMessage struct {
	Role string `json:"role"`
	Content string `json:"content"`
}

func NewMessage(phone string, botRole string, role string, content string, time time.Time) Message {
	var message Message
	message.Phone = phone
	message.BotRole = botRole
	message.Role = role
	message.Content = content
	message.Time = time
	return message
}

func NewSimpleMessage(role string, content string) SimpleMessage {
	return SimpleMessage {
		Role: role,
		Content: content,
	}
}

func (msg *Message) ToSimpleMessage() SimpleMessage {
	return NewSimpleMessage(msg.Role, msg.Content)
}

func AddMessages(messages *[]Message) error {
	return DB.Create(&messages).Error
}

func GetNewestMessage(phone string, number int, size int) ([]Message, error) {
	var message []Message
	err := DB.Order("time").Limit(number).Offset(size).Where("phone = ?", phone).Find(&message).Error
	// reserve array
	// for i, j := 0, len(message)-1; i < j; i, j = i+1, j-1 {
	// 	message[i], message[j] = message[j], message[i]
	// }
	return message, err
} 