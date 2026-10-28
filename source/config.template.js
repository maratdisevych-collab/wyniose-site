/* Wyniosę: контакты и данные фирмы. Если что-то поменялось, правьте здесь и загрузите файл на хостинг заново.
   phone      главный номер: «Zadzwoń» и WhatsApp, например "+48 600 123 456"
   phone2     второй номер (показывается в подвале), можно оставить ""
   whatsapp   только если WhatsApp на другом номере, чем phone, иначе ""
   email      адрес для связи
   company    данные фирмы для подвала и политики конфиденциальности: name, address, nip, regon
   privacyUrl ссылка на политику конфиденциальности
   privacyDate дата последней правки политики
   ads        Google Ads, работает только после согласия посетителя (баннер cookie):
              id  = тег AW-…, tel = ярлык «Telefon», wa = ярлык «WhatsApp».
              Чтобы выключить измерение совсем, удалите блок ads: баннер тоже исчезнет. */
window.SITE = {
  phone: "",
  phone2: "",
  whatsapp: "",
  email: "",
  company: {name: "", address: "", nip: "", regon: ""},
  privacyUrl: "/polityka-prywatnosci/",
  privacyDate: "",
  ads: {id: "", tel: "", wa: ""}
};
