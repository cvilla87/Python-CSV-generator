# Python CSV generator

## What
A simple tool to generate fake but **realistic** data.


## Why
I wanted something fast and simple to generate a custom dataset, and at the same time flexible
so in the future I can make more modifications to fit the needs of some specific use case.
 
I did some research about existing tools and found [Mockaroo](https://mockaroo.com/) and [generatedata](https://www.generatedata.com/), 
along with many others that either were not free or were only focused on some specific database engine.<br>
In the two mentioned it's not possible to generate any big dataset for stress testing purposes, since they have a limit 
on the number of rows (1000 and 100 respectively). You can create an account to increase that limit or, even better, 
in the 2nd option you can download the open source tool. But even with that I found some limitations that I resolved 
with a better solution.

With the Python library [Faker](https://faker.readthedocs.io/en/master/) I had many more possibilities such as:
  - Create fake data for many different **locales** (de_DE, en_GB, en_US, it_IT, fi_FI, es_ES, pl_PL, etc.).<br>
  This will create realistic names, real addresses, phone numbers, name of companies, vehicle registration plates...<br>
  More about Faker locales: https://faker.readthedocs.io/en/master/locales.html
  - Create a **real GPS position** (latitude + longitude), with an option to set the country.<br>
  Other tools create a totally random latitude and longitude, these being separated columns independent of each other, 
  thus the result of the location can be anywhere.
  - Random **timestamps within a specified threshold** (number of days back from which it should be created).
  - **Relationship between rows**: Because it uses a [seed](https://faker.readthedocs.io/en/master/index.html#seeding-the-generator)
   functionality (more on this later), you can define total random values or get one exact value.
   This functionality helps you create a dataset in which you can have thousands of rows for the same person 
   (same name but differences in other columns), which allows you to track their data through all their rows. 


## How to modify `config.ini`
The ini file has different section headers (enclosed by `[]`), each one with their own `key=value` pairs (options).

The list of options that can be modified from `MAIN` section are the following:
 - **sep**: Indicates the character that will be used as a delimiter/separator of the columns.
 - **lines**: Number of lines that will be generated for the dataset.
 - **header** [boolean**¹**]: Indicates whether header should be included.
 - **dataset**: Name of the dataset structure that it will be used. If the one provided doesn't exist, 
 it will be used the `dummy` structure.
 - **switch_locale** [boolean**¹**] (Faker mode only): Indicates whether locale should be randomly switched from the provided list.
 - **days_back** (Faker mode only): It indicates the number of days back from which timestamp 
 should be created (until current day).
 - **locales** (Faker mode only): List of locales that is going to be used by Faker.<br>
 By default, it has been included a list of 18 locales that are accepted by Faker.
 It is possible to modify this option value by deleting some, adding new ones, or even leaving only 1 locale, 
 so all the data will be generated for the same locale.<br>
 If the goal is to leave only 1 locale, it makes sense to disable `switch_locale` option.
 - **custom_datatypes** (Faker mode only): These datatypes are special because when you call it via Faker, 
 you need to provide some argument, otherwise it will raise an *AttributeError* exception. 
 Depending on the Faker [providers](https://faker.readthedocs.io/en/master/providers.html), the argument sometimes 
 could be an integer (to indicate number of days), sometimes a string (to indicate country)...<br>
 Unless you want to use a new call to the Faker API that requires some argument (most of them don't require it),
 you don't need to add any other custom datatype to this option.
 
**¹** In Python's config parser, accepted **booleans** values are `yes`/`no`, `on`/`off`, `true`/`false` and `1`/`0`.


### Creating a new dataset structure
In order to create a new dataset structure we have first to understand the different parts of it:

    [dataset_structure_name]
    key1 = value1
    [...]
    keyN = valueN

It is important to notice here about the difference in the values between `dummy` and the other datasets.<br>
While for `dummy` it uses only integers that will follow a single hardcoded behaviour, for all other datasets 
specific values will be needed, and they will follow the **Faker** behaviour.<br>
Here are the main differences:

| Structure  | Key         | Value         |
|:---------- |:------------|:--------------|
| dummy      |  It is used as the header in the generated dataset. | Only integers are accepted. They are used to indicate the length of the random text (`string.ascii_letters`).  |
| All others |  *Same as in dummy* | Name of one of the Faker generator properties (these are packed inside [providers](https://faker.readthedocs.io/en/master/providers.html)). In case the provider generator doesn't exist for the indicated value, `text` will be used to generate random fake text. |

The only time that is needed to modify the code is when adding some Faker generator that requires some argument.<br>
If that's the case, `custom_datatypes` option needs to be modified to add the name of a valid Faker provider and the code must be 
adapted in the same way as for in the other cases. 


## How to use Seed
This is one of the functionalities that it will probably require some tweaking to get the dataset that we are expecting.

Faker seeding allows to generate the same result when using the same seed value. But it also may be used to generate more 
random values. The general idea is: The smaller range for the seed, the more probability of repeated values.<br>

For example, the explanation of some of the tweaks that has been done in the code: 

| Code       | When      | Reason  |
|:---------- |:------------|:--------------|
| `fake.seed_instance(random.randint(0, 4))`    | Before calling the provider generators. | To use a list of 5 possible results, so we can track them along the dataset. |
| `fake.seed_instance(random.randint(0, 5000))` | Used for timestamp. | To get completely different values, avoiding repeated values. |


More info: https://faker.readthedocs.io/en/master/index.html#seeding-the-generator


## Example of output data
- `dummy` dataset:
    ```
    hxlWaZksCuzpXEefvBHLPOcFqbmVDT|FdvxjUytfl|f|nQFRHzqeBDLwOfPXGhoi|uYQdz
    hpKzmTvgfCxOZknNXQiqrwDdVjWesI|eWAluBsNxm|q|HMopieGPbDsvcrQqjEXO|JOuUc
    lIvOsDBhGQCLXanSwUxHqgcNfVtidb|oYGpqrekDI|m|fODszYeuRAGxkHPCLKhZ|buBFV
    OSKLdCMHPjqAahfkvsnxVtYWgzTRyD|SOWULTiIcy|p|bVoEBirQeCPUdfDyqkXm|MJvfx
    OKjMDAVTCwmJHuNYqhgLoQxBErepsy|hfOSMnRDmK|f|sYRnmSZuxLhtVbPKWcal|dafxG
    ```

- `creditcard` dataset:
    ```
    Véronique Bertrand de Guibert|49, chemin Grégoire Marques 85878 Leroy|630456682826|03/23|VISA 16 digit|899.42|2019-02-08 19:57:04|('48.77275', '5.16108')
    Véronique Bertrand de Guibert|49, chemin Grégoire Marques 85878 Leroy|630456682826|03/23|VISA 16 digit|1593.72|2019-02-21 19:11:12|('45.73333', '4.91667')
    Julien Herve|1, chemin de Perret 78876 Lemaireboeuf|4012904047966693|09/26|JCB 16 digit|2052.73|2018-12-15 11:51:51|('44.80477', '-0.59543')
    Stéphane Godard|46, rue Guibert 07439 Fischer-sur-Laurent|675963608376|08/27|Discover|942.36|2019-01-19 08:56:37|('48.79325', '2.29275')
    Véronique Bertrand de Guibert|49, chemin Grégoire Marques 85878 Leroy|630456682826|03/23|VISA 16 digit|2513.6|2018-12-17 11:59:14|('45.73333', '4.91667')
    ```
Notice how, because of the Seed tweaking done in the code, there are repeated values for name and address 
but not for timestamps or GPS location.


## Performance
Using an `Intel Core i7 8750H` for the tests, I got the following results:<br>

    dummy
        30k rows in 2.1 seconds
        500k rows in 36 seconds
        1M rows in 72 seconds
    creditcard (Faker)
        30k rows in 12 seconds (without changing locale)
        30k rows in 26 seconds (changing locale every 100 records)
        30k rows in 1880 seconds (changing locale at every record)

From the previous timing I considered that it works better changing the locale every 100 rows.<br>
It's pretty obvious that changing the locale at every row is an overkill when you are generating a big dataset.


## Suggestions / Improvements
These are some ideas that I thought about implementing but I couldn't finish:
  - **Progress indicator**: Every 5, 10, 25%... of the created lines write output to indicate the current progress.  
  - Refactorization.

Feel free to send me some :cool: Pull Requests :snowman:

PS: I'm aware I didn't go too crazy in terms of **input validation**, but it's not the idea to overcomplicate and make
this simple script longer with too many validations.


## References
https://faker.readthedocs.io/en/master/
