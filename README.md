IP Konum Bilgisi Sorgulama Dokümantasyonu

Bu betik, bir IP adresi veya domain hakkında coğrafi konum bilgisi sağlamak için tasarlanmıştır. Aşağıda kodun ayrıntılı açıklaması ve belirli unsurların neden uygulandığı açıklanmaktadır.

Kullanılan Kütüphaneler

requests: ipinfo.io üzerinden coğrafi konum bilgisi almak için HTTP istekleri yapar.

sys: Sistem argümanları ve çıkış koşulları ile etkileşim kurmak için kullanılır.

re: İthal edilmiş fakat şu anda kullanılmıyor. Gerekirse regex doğrulaması için kullanılabilir.

logging: Hata mesajlarını bir dosyaya (error_log.txt) kaydetmek ve gerçek zamanlı olarak konsolda log tutmak için kullanılır.

json: Önbelleğe alınan bilgileri okumak ve yazmak için JSON verilerini işler.

argparse: Orijinal olarak komut satırı argümanlarını ayrıştırmak için kullanıldı, basitlik açısından sys.argv ile değiştirildi.

socket: Domain isimlerini IP adreslerine çözümlemek için kullanılır.

ipaddress: Girilen bilginin geçerli bir IP adresi olup olmadığını doğrulamaya yardımcı olur.

hashlib: Önbelleğe alınan yanıtları etkili bir şekilde saklamak/almak için bir hash anahtarı oluşturur.

os: Önbellek dosyasının var olup olmadığını kontrol etmek için kullanılır.

Önbellek Yönetimi

CACHE_FILE: Önbellek dosyasının (ip_cache.json) adını saklayan bir sabit. Bu dosya, daha önce alınmış IP bilgilerini saklamak için kullanılır ve tekrarlayan ağ isteklerine olan ihtiyacı azaltır.

load_cache(): ip_cache.json dosyasından önbelleğe alınmış verileri yükler (eğer mevcutsa). Bu, ağ trafiğini azaltmak ve daha hızlı yanıtlar sağlamak için önemlidir.

save_cache(cache): Geçerli önbellek sözlüğünü ip_cache.json dosyasına kaydeder. Bu, ipinfo.io'ya yapılan tekrarlayan istekleri azaltmaya yardımcı olur ve sonraki aynı sorgularda hız kazandırır.

Fonksiyon Açıklamaları

check()

Amacı: Bu fonksiyon, ipinfo.io hizmetinin çevrimiçi olup olmadığını kontrol etmek için temel URL'ye bir istek gönderir.

Uygulama: Sunucu erişilebilir durumdaysa (status_code 200), sunucunun çevrimiçi olduğunu belirtir. Aksi takdirde bir hata yükseltir ve log tutar. Bu, hizmetin kullanılabilirliğini önceden kontrol ederek gereksiz sorguları ve olası hataları önlemek amacıyla eklenmiştir.

main(ip_or_domain)

Log Yapılandırması: Hem bir dosyaya (error_log.txt) hem de konsola StreamHandler kullanarak hata loglamayı başlatır. Bu, hataların gerçek zamanlı olarak izlenmesini ve daha sonra gözden geçirilmesini sağlar. Hataların hem dosyada hem de konsolda görünmesi, geliştirme ve hata ayıklama süreçlerini daha verimli hale getirir.

Önbellek Yükleme: Daha önce yapılan sorguların tekrar yapılıp yapılmadığını kontrol etmek için önbelleğe alınmış IP verilerini yükler. Eğer varsa, önbellekteki sonucu gösterir. Bu, gereksiz ağ isteklerini önler ve performansı artırır.

IP Adresi veya Domain İşleme:

İlk olarak, ipaddress modülü kullanılarak girdinin geçerli bir IP adresi olup olmadığını belirlemeye çalışır. Bu, kullanıcının hatalı bir IP adresi girmesi durumunda zaman kaybetmemek adına önemlidir.

Girdi geçerli bir IP değilse, socket.gethostbyname() kullanarak domain adını bir IP'ye çözümlemeye çalışır. Eğer bu başarısız olursa, ValueError yükseltir ve kullanıcıyı bilgilendirir.

Özel IP Kontrolü: Kod, verilen IP adresinin özel/yerel bir IP (örneğin 192.168.x.x, 10.x.x.x veya 172.16.x.x - 172.31.x.x) olup olmadığını kontrol eder. Eğer öyleyse, kullanıcının geçerli bir genel IP girmesini ister. Bu, sadece genel IP'ler üzerinde çalışılması gerektiği durumlar için eklenmiştir.

Çevrimiçi Kontrolü: İşleme devam etmeden önce ipinfo.io'nun çevrimiçi olup olmadığını kontrol etmek için check() fonksiyonunu çağırır. Bu, ağ bağlantı sorunlarını erkenden tespit etmeye yardımcı olur.

Önbelleğe Alma ve İstek İşleme:

Önbellek Anahtarı: IP veya domain isminden bir hash anahtarı oluşturmak için hashlib.md5 kullanır. Bu, önbellek girdilerinin saklanmasını ve alınmasını kolaylaştırır ve hızlı erişim sağlar.

Önbellekte bir giriş bulunursa, önbelleğe alınmış sonucu yazdırır. Bu, daha önce yapılan sorguların tekrarlanmasını önler.

Aksi takdirde, ipinfo.io'ya coğrafi konum verisi almak için bir istek gönderir, yanıtı önbelleğe alır ve sonucu yazdırır. Hatalar uygun şekilde loglanır ve kullanıcının bilgilendirilmesi sağlanır.

__main__ Bloğu

Etkileşimli Döngü: Betik, kullanıcının bir IP adresi veya domain adı girmesine olanak tanıyan bir döngüye girer. Bu, kullanıcıya ardışık olarak farklı IP veya domain sorgulamaları yapma esnekliği sağlar.

Komut Satırı Argümanları: Betik çağrılırken bir IP adresi veya domain sağlanmışsa, sağlanan girişle bir kez çalışır ve çıkar. Bu, betiğin komut satırından otomatik olarak kullanılabilmesini sağlar.

Döngü Devamı: Her sorgudan sonra kullanıcıdan başka bir IP veya domain girmesi istenir (e/h). Kullanıcı 'e' yazarsa betik başka bir sorgu çalıştırır; aksi halde çıkar. Bu, betiğin kullanıcı dostu olmasını sağlar ve kullanıcıya birden fazla sorgu yapma imkanı verir.

Özet

Bu betik, IP veya domain coğrafi konum sorgularını şu şekilde etkili bir şekilde ele alır:

Yanıtların Önbelleğe Alınması: Yanıtları saklar, böylece tekrarlayan ağ isteklerini en aza indirir ve performansı artırır. Bu sayede aynı IP veya domain için yapılan tekrarlı sorgularda zaman kazandırır.

Loglama: Hem konsola gerçek zamanlı görünürlük hem de sonradan analiz için dosyaya sağlam bir hata loglama sağlar. Bu, hem geliştirici hem de kullanıcı için daha iyi hata yönetimi sunar.

Doğrulama ve Esneklik: Hem IP adreslerini hem de domain isimlerini doğrular ve gereksiz sorguları önlemek için özel IP aralıklarını kontrol eder. Bu sayede sadece geçerli ve genel IP'ler üzerinde işlem yapılmasını sağlar.

Kullanıcı Deneyimi: Döngü, kullanıcıların programı yeniden başlatmadan birden fazla sorgu yapmasına olanak tanır, bu da tekrarlanan kontroller için kullanışlıdır. Kullanıcıya her sorgudan sonra başka bir sorgu yapma imkanı tanınır, bu da kullanıcı deneyimini geliştirir.

Bu özellikler, betiği kullanıcı dostu ve IP coğrafi konum verilerini almak açısından verimli hale getirirken, harici hizmetlere olan yükü azaltır ve sorun durumunda anlamlı loglar sağlar. Ayrıca, önbellekleme ve hataların konsolda görüntülenmesi gibi özellikler, hem performansı hem de kullanıcı geri bildirimini artırır.
