package goscripts

import (
	"net/url"
	"strings"
)

func ModifyUrlParam(u string, param map[string]string) (string, bool) {
	urlStruct, err := url.Parse(u)
	if err != nil {
		return u, false
	}
	if len(param) == 0 {
		return u, true
	}
	queryArr := urlStruct.Query()
	for k, v := range param {
		queryArr.Set(k, v)
	}
	urlStruct.RawQuery = queryArr.Encode()
	return urlStruct.String(), true
}

func GetUrlHost(u string) string {
	urlStruct, err := url.Parse(u)
	if err != nil {
		return ""
	}
	return urlStruct.Hostname()
}

func TrimUrlHost(u string) string {
	us := strings.TrimPrefix(u, "https://")
	return strings.TrimPrefix(us, "http://")
}
