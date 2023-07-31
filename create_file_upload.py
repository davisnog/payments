from faker import Faker
import csv

def create_line():
    fake = Faker('pt_BR')
    return {
        'name': fake.name(),
        'governmentId': fake.cpf().replace('.', '').replace('-', ''),
        'email': fake.email(),
        'debtAmount': fake.pydecimal(positive=True, right_digits=2, max_value=1000000),
        'debtDueDate': fake.date(),
        'debtId': fake.pyint()
    }


if __name__ == '__main__':
    field_names= ['name', 'governmentId', 'email', 'debtAmount', 'debtDueDate', 'debtId']

    with open('upload_large.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()

        for n in range(12000):
            row = create_line()
            writer.writerow(row)
