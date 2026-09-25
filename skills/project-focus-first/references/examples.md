# Project Focus First — Examples

> Loaded on demand by `project-focus-first`.

## Example 1: New application

User:

> Yapay zekâ destekli bir eğitim uygulaması geliştirmek istiyorum.

Assistant:

> Bu çalışma için öncelikli odak noktamız hangisi?
>
> 1. Ürün  
> 2. Marketing / Büyüme  
> 3. Mühendislik / Teknik  
> 4. Araştırma / Keşif  
> 5. Validasyon  
> 6. Tasarım / Kullanıcı Deneyimi (UX)  
> 7. Monetizasyon / İş Modeli  
> 8. Operasyon / Sürdürülebilirlik  
>
> Bir numara veya kategori adıyla cevaplayabilirsin. Birden fazla alan önemliyse birini **ana odak**, diğerini **ikincil odak** olarak belirt.

Stop.

## Example 2: Premature technology request

User:

> Bir SaaS fikrim var. React mı Next.js mi kullanmalıyım?

Assistant asks the focus question. It does not compare React and Next.js yet.

## Example 3: Explicit focus in the first message

User:

> Bir iş takip uygulaması geliştireceğim. Öncelikle fikri doğrulamak istiyorum.

Assistant:

> Ana odak: **Validasyon**

Then answer the user's request through validation, without repeating the focus question.

## Example 4: Equal priorities

User:

> Ürün ve teknik birlikte önemli.

Assistant:

> İkisini de ele alabiliriz; ancak hangisi birincil odak olacak? Diğerini ikincil odak olarak koruyabiliriz.

Stop.

## Example 5: New project in the same conversation

The active project is an AI résumé tool with primary focus `Ürün`.

User:

> Şimdi de restoranlar için rezervasyon sistemi geliştirmek istiyorum.

Assistant treats this as a new project and asks the focus question again.

## Example 6: Isolated bug fix

User:

> Bu SQL sorgusundaki ORA-00904 hatasını düzelt.

Assistant does not trigger this skill. It handles the scoped bug.
