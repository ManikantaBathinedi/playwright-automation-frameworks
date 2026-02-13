using Bogus;

namespace PlaywrightFramework.Utilities;

/// <summary>
/// Test data generator using Bogus library
/// </summary>
public static class DataGenerator
{
    private static readonly Faker Faker = new();

    // Email
    public static string RandomEmail() => Faker.Internet.Email();
    public static string RandomCompanyEmail(string company) => Faker.Internet.Email(provider: company);

    // Strings
    public static string RandomString(int length = 10) => Faker.Random.AlphaNumeric(length);
    public static string RandomText(int words = 10) => Faker.Lorem.Words(words).ToString() ?? string.Empty;
    public static string RandomSentence() => Faker.Lorem.Sentence();
    public static string RandomParagraph() => Faker.Lorem.Paragraph();

    // Numbers
    public static int RandomNumber(int min = 0, int max = 100) => Faker.Random.Int(min, max);
    public static decimal RandomDecimal(decimal min = 0, decimal max = 1000) => Faker.Random.Decimal(min, max);

    // Dates
    public static DateTime RandomDate() => Faker.Date.Recent();
    public static DateTime RandomFutureDate() => Faker.Date.Future();
    public static DateTime RandomPastDate() => Faker.Date.Past();

    // Names
    public static string RandomFirstName() => Faker.Name.FirstName();
    public static string RandomLastName() => Faker.Name.LastName();
    public static string RandomFullName() => Faker.Name.FullName();

    // Passwords
    public static string RandomPassword(int length = 12) => Faker.Internet.Password(length);
    public static string GenerateStrongPassword() => Faker.Internet.Password(16, memorable: false, prefix: "Aa1!");

    // Phone
    public static string RandomPhoneNumber() => Faker.Phone.PhoneNumber();

    // Address
    public static string RandomAddress() => Faker.Address.FullAddress();
    public static string RandomCity() => Faker.Address.City();
    public static string RandomZipCode() => Faker.Address.ZipCode();
    public static string RandomCountry() => Faker.Address.Country();

    // Company
    public static string RandomCompanyName() => Faker.Company.CompanyName();

    // Internet
    public static string RandomUrl() => Faker.Internet.Url();
    public static string RandomUsername() => Faker.Internet.UserName();

    // Credit Card
    public static string RandomCreditCardNumber() => Faker.Finance.CreditCardNumber();
    public static string RandomCreditCardCvv() => Faker.Finance.CreditCardCvv();

    // Complete User Object
    public static User GenerateUser()
    {
        return new User
        {
            FirstName = RandomFirstName(),
            LastName = RandomLastName(),
            Email = RandomEmail(),
            Password = GenerateStrongPassword(),
            Phone = RandomPhoneNumber(),
            Address = RandomAddress(),
            City = RandomCity(),
            ZipCode = RandomZipCode(),
            Country = RandomCountry()
        };
    }
}
