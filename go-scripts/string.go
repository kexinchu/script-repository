package goscripts

import (
	"html"
	"reflect"
	"regexp"
	"strings"
	"unicode/utf8"
)

// FilterContent 字符串过滤
func FilterContent(strContent string) string {
	var strRes string
	var replacer *strings.Replacer
	replacer = strings.NewReplacer("</b>", "", "<b>", "", "<br>", "", "</br>", "", "<br/>", "",
		"<span>", "", "</span>", "", "bd-data-layer=&quot;1&quot;&gt;1、", "", "bd-data-layer=&quot;1&quot;&gt;1", "")
	strRes = replacer.Replace(strContent)

	// 正则
	var reg *regexp.Regexp
	reg = regexp.MustCompile(`<a.*</a>`)
	strRes = reg.ReplaceAllString(strRes, "")

	replacer = strings.NewReplacer(`"`, "", "&quot", "", "&lt;br&gt;", "", "&lt;br/&gt", "", "&gt;", "")
	strRes = replacer.Replace(strRes)
	strRes = strings.Trim(strRes, ":")

	reg = regexp.MustCompile(`<[^>]+>`)
	strRes = reg.ReplaceAllString(strRes, "")

	strRes = html.UnescapeString(strRes)

	reg = regexp.MustCompile(`<[^>]+>`)
	strRes = reg.ReplaceAllString(strRes, "")

	l := utf8.RuneCountInString(strRes)
	if l-2 == StrPosRune(strRes, "2、", 0) {
		strRes = strings.ReplaceAll(strRes, "2、", "")
	}
	if l-2 == StrPosRune(strRes, "3、", 0) {
		strRes = strings.ReplaceAll(strRes, "3、", "")
	}
	if l-2 == StrPosRune(strRes, "。2", 0) {
		strRes = strings.ReplaceAll(strRes, "。2", "")
	}
	return strRes
}

//中文，字符串片段在字符串中首次出现的位置，支持设置偏移量
func StrPosRune(str, sub string, off int) int {
	if off < 0 {
		return -1
	} else if off == 0 {
		pos := strings.Index(str, sub)
		if pos == -1 {
			return -1
		}
		head := str[:pos]
		hl := utf8.RuneCountInString(head)
		return hl
	} else {
		var p int
		for {
			pos := strings.Index(str, sub)
			if pos == -1 {
				return -1
			}
			head := str[:pos]
			hl := utf8.RuneCountInString(head)
			p += hl
			if p >= off {
				return p
			} else {
				str = str[pos+len(sub):]
				p += utf8.RuneCountInString(sub)
			}

		}
	}
}

//中文，字符串片段在字符串中的位置，不区分大小写
func StrIPosRune(str, sub string) int {
	str = strings.ToUpper(str)
	sub = strings.ToUpper(sub)
	pos := strings.Index(str, sub)
	if pos == -1 {
		return -1
	}
	head := str[:pos]
	hl := utf8.RuneCountInString(head)
	return hl
}

//中文取子串，支持设置偏移量
func SubStrRune(str string, start, off int) string {
	if off < 0 {
		return ""
	}
	if start < 0 {
		start = utf8.RuneCountInString(str) - (-start)
	}
	startIndex := -1
	endIndex := -1
	cur := 0
	for i := range str {
		if cur == start {
			startIndex = i
		}
		//不设置偏移量，直接返回剩下的部分
		if startIndex >= 0 && off == 0 {
			return str[startIndex:]
		}
		if startIndex >= 0 && start+off == cur {
			endIndex = i
			return str[startIndex:endIndex]
		}
		cur++
	}
	//偏移量超出了字符串长度直接把剩下的都返回去
	if startIndex >= 0 {
		return str[startIndex:]
	}
	return ""

}

//中文字符串最后一次出现的位置
func StrRPosRune(str, sub string) int {
	var p, last int
	for {
		pos := strings.Index(str, sub)
		if pos == -1 {
			if last == 0 {
				return -1
			} else {
				return last
			}
		}
		head := str[:pos]
		hl := utf8.RuneCountInString(head)
		p += hl
		//记下最后一次的标记
		last = p
		str = str[pos+len(sub):]
		p += utf8.RuneCountInString(sub)
	}
}

func InsertSubStrRune(str, sub string, pos int) string {
	if pos <= 0 {
		return sub + str
	}
	var cur int
	for i := range str {
		if cur == pos {
			return str[:i] + sub + str[i:]
		}
		cur++
	}
	return str + sub
}

func IsValidStr(val string) bool {
	if val == "-" || val == "" {
		return false
	}
	return true
}

// IsValid 判断字段是否有效
func IsValid(val interface{}) bool {
	if Empty(val) {
		return false
	}
	// 建库数据会补充 "-"
	strVal, ok := val.(string)
	if !ok || strVal == "-" {
		return false
	}
	return true
}

// Empty 判断是否为空
func Empty(val interface{}) bool {
	v := reflect.ValueOf(val)
	switch v.Kind() {
	case reflect.String, reflect.Array:
		return v.Len() == 0
	case reflect.Map, reflect.Slice:
		return v.Len() == 0 || v.IsNil()
	case reflect.Bool:
		return !v.Bool()
	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
		return v.Int() == 0
	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
		return v.Uint() == 0
	case reflect.Float32, reflect.Float64:
		return v.Float() == 0
	case reflect.Interface, reflect.Ptr:
		return v.IsNil()
	}
	return reflect.DeepEqual(val, reflect.Zero(v.Type()).Interface())
}

func Min(a, b int, c ...int) int {
	if c == nil {
		if a < b {
			return a
		} else {
			return b
		}
	} else {
		c = append(c, a, b)
		min := 0
		for i, v := range c {
			if i == 0 {
				min = v
			}
			if v < min {
				min = v
			}
		}
		return min
	}
}
