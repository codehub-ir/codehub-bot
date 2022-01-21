<p align="center">
    <img width="140" src="https://raw.githubusercontent.com/codehub-ir/codehub-graphics/0dd43fd4d2f145f511332f09cc415acffe9e6637/github-org/SVGs/logotype-170.svg" />
</p>

<p align="center">
    <h1 align="center">
        <a href="https://codehub.pythonanywhere.com/" dir="rtl">ربات تلگرام کدهاب (V2.0)</a>
    </h1>
</p>

[English](./README.md) | فارسی

<div dir="rtl">
یک رابط با تلگرام و کتابخانه python-telegram-bot که می‌توانید با آن، برنامه خود را  پیست کنید، پیدا کنید و به اشتراک بذارید.

## موارد لازم

موارد لازم `requirements.txt`:

<div dir="ltr">

1. python-telegram-bot
2. python-dotenv
3. peewee

</div>

## استفاده

1. نیازمندی‌ها را نصب کنید:

<pre dir="ltr">
pip install -r requirements.txt
</pre>

2. یک فایل `.env` (در کنار `main.py`) بسازید که محتوی آن به شکل زیر باشد:

<pre dir="ltr">
TOKEN="..."
WEBHOOK="..."
</pre>

<div dir="rtl">
    مقدار <code>TOKEN</code> را برابر با توکن ربات خود قرار دهید. می‌توانید توکن را از <code dir="ltr">@botfather</code> دریافت کنید.
اگر می‌خواهید از وبهوک استفاده کنید، مقدار <code>WEBHOOK</code> را برابر با آدرس مورد نظر قرار دهید. وگرنه، خالی بذارید (<code dir="ltr">WEBHOOK=""</code>)

</div>

3. و بلاخره...

<pre dir="ltr">python3 main.py</pre>

<div dir="rtl">
    ممکن است که بخواهید از مواردی مانند <code>tmux</code> برای اجرای ربات استفاده کنید؛ مثلا هنگام استفاده از سرور.
</div>

<br />

<div dir="rtl">
    توجه: این ربات از <code>sqlite3</code> برای ذخیره داده‌های پیست‌ها، چت‌ها و کاربران استفاده می‌کند. اگر می‌خواهید از مواردی مانند <code>MySQL</code> یا <code>PostgreSQL</code> استفاده کنید، باید در <code dir="ltr">src/model/__init__.py</code>. تغییراتی ایجاد کنید. <a href="http://docs.peewee-orm.com/en/latest/peewee/database.html">مستندات peewee</a> را ببینید.
</div>

## Contributing

با اینکه بخش‌های مختلفی در اینجا وجود دارد، با این حال، شما بیشتر روی دو بخش باید تمرکز کنید:

1. `src/handler`

    این پوشه، Handlerهای لازم را داراست. هر Hanlder یک پوشه ویژه خود به شکل <code dir="ltr">src/handler/&lt;NAME&gt;</code> داراست. Handler مورد نظر در <code dir="ltr">src/handler/&lt;NAME&gt;/\_\_init\_\_.py</code> تعریف خواهد شد. در این فایل، شما باید تابعی به شکل <code dir="ltr">creator(model)</code> تعریف کنید. پارامتر <code>model</code>، در واقع ایمپورت شده <code dir="ltr">src/model</code> می‌باشد. این تابع، با دریافت این پارامتر، دقیقا یک شی Handler برمی‌گرداند. شما می‌توانید هر تعداد پوشه حاوی Handlerهای مختلف بسازید.

    برای نمونه، فرض می‌کنیم که یک Handler برای دریافت <code dir="ltr">/start</code> می‌خواهید بنویسید. در این صورت، باید یک پوشه و یک فایل <code dir="ltr">\_\_init\_\_.py</code> درون آن بسازید؛ مانند <code dir="ltr">src/handler/my_start_handler/\_\_init\_\_.py</code> بسازید، سپس محتوی آن، برای مثال، می‌تواند به شکل زیر باشد


<pre dir="ltr">
    from telegram.ext import CommandHandler, CallbackContext
    from telegram import Update

    def your_function(update: Update, context: CallbackContext):
        update.message.reply_text("hello!")

    def creator(model):
        return CommandHandler("start", your_function)
    </pre>

<div dir="rtl">
    با این حال، شاید شما بخواهید که از یک ‌attributeای درون <code dir="ltr">src/model</code> مانند <code dir="ltr">HELLO_TEXT</code> استفاده کنید. پیشنهاد می‌کنیم که یک تابع برای پاس دادن مدل استفاده کنید. این تابع از قبل درون <code dir="ltr">src/handler/functions.py</code> نوشته شده است. پس، می‌توانید به این شکل از آن استفاده کنید:
</div>

<br />

<pre dir="ltr">
    from telegram.ext import CommandHandler, CallbackContext
    from telegram import Update
    from ..function import pass_model_to

    def your_function(update: Update, context: CallbackContext, model):
        update.message.reply_text(model.HELLO_TEXT)

    def creator(model):
        return CommandHandler("start", pass_model_to(your_function, model))
</pre>

<div dir="rtl">
    اگر شما توابع/کلاس‌هایی دارید که می‌خواهید از آن‌ها در Handlerهای متنوعی استفاده کنید، می‌توانید درون <code dir="ltr">src/handler/functions.py</code> بگذارید؛ سپس import کنید.
</div>

<br />

<div dir="rtl">
    وقتی کار نوشتن Handler تمام شد، باید <code>creator</code> آن را در <code dir="ltr">src/handler/__init__.py</code> import کنید و به تاپل <code>CREATORS</code> اضافه کنید. بعنوان مثال، اگر می‌خواهید که Handler مورد بحث، یعنی <code>my_start_handler</code> را اضافه کنید؛ باید این خط را به <code dir="ltr">src/handler/__init__.py</code> اضافه کنید:
</div>

<br />

<pre dir="ltr">
from my_start_handler import creator as my_start_handler_creator
</pre>

<div dir="rtl">

همانطور که می‌بینید، وقتی که Handlerای به نام <code>&lt;NAME&gt;</code> را می‌خواهیم اضافه کنیم، بهتر است <code>creator</code> آن، به شکل <code dir="ltr">&lt;NAME&gt;\_creator</code> استفاده شود (<code dir="ltr">from &lt;NAME&gt; import creator as &lt;NAME&gt;_creator</code>). سپس، آنرا به تاپل <code>CREATORS</code> اضافه می‌کنیم.

برای نمونه، سه Handler زیر را تصور کنید:
<ul dir="ltr">
 <li><code>handler1</code> (<code dir="ltr">src/handler/handler1</code>)</li>
 <li><code>handler2</code> (<code dir="ltr">src/handler/handler2</code>)</li>
 <li><code>handler3</code> (<code dir="ltr">src/handler/handler3</code>)</li>
</ul>

حال، در این مثال، اگر بخواهیم همه را بکار ببریم، باید <code dir="ltr">src/handler/\_\_init\_\_.py</code> را به شکل زیر بنویسیم:

</div>

<pre dir="ltr">
from handler1 import creator as handler1_creator
from handler2 import creator as handler2_creator
from handler3 import creator as handler3_creator
# from your_new_handler import creaotr as your_new_hanlder_creator

CREATORS = (
    handler1_creator,
    handler2_creator,
    handler3_creator,
    # your_new_hanlder_creator,
)

# don't change it, don't remove it, don't see it, and don't think about it at all!
def get_handlers(model):
    for creator in CREATORES:
        yield creator(model)
</pre>

<div dir="rtl">
    *توجه: اگر Handler خود را به این شکل اضافه نکنید، Handler شما به <code>dispatcher</code> اضافه نخواهد شد. اگر دیدید که Handler شما کار نمی‌کند (با فرض اطمینان از نحوه کارکرد Handler خود و واکنشِ بدون ایرادِ ربات به سایر Handlerها)، احتمالا بخاطر این است که آن را اضافه نکردید!
</div>

<br />

2. `src/model`

این بخش، هر داده‌ای در رابطه با زبان‌ها (فارسی، انگلیسی، ...)، database و ... را در بر می‌گیرد. در حال حاضر، همین دو مورد گفته شده در آن قرار دارد. این بخش، import شده و به creatorهای handlerها داده می‌شود (پارامتر <code>model</code> در <code dir="ltr">creator(model)</code>، یادته دیگه؟!). برای مثال، اگر <code dir="ltr">EXAMPLE = 123</code> را در <code dir="ltr">src/model/\_\_init\_\_.py</code> تعریف کنید؛ می‌توانید از طریق پارامتر <code>model</code>، به شکل <code dir="ltr">model.EXAMPLE</code> از آن استفاده کنید.

</div>
