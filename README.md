# Voti.py

This script is designed to help students at "Politecnico di Bari" manage their exam grades and compute their starting
grade for graduation. It also allows for the simulation of the impact of a single grade on the overall average.

## Features

- **Add Exam**: Add a new exam to the list.
- **Remove Exam**: Remove an exam from the list.
- **Compute Starting Grade**: Calculate the starting grade for graduation based on the current exams.
- **Reset Exams**: Reset all exam grades and dates.
- **Simulate Exam**: Simulate the impact of a single grade on the overall average, without saving it.

## Usage

The script is based on the configuration file `exams.json`, used to keep track of the exams (grade, CFU, date).
Moreover, at the end of the file there are other parameters that can be modified:

- `anni_fuori_corso`: the number of years out of course.
- `cfu_off`: the number of CFU that can be excluded from the calculation (9 for LM, 12 for LT).
- `alpha`: the weight of the final exam (0 - 0.08).

Regarding the `lodi` parameter, it is computed automatically by the script by counting the number of exams with a grade
of 30 cum laude. Notice that:

- **to register a 30L, the student has to write 31**.
- **a 31 is still considered as a 30 in the average computation**.

Here it is the template of the configuration file:

```json
{
  "exams": [
    {
      "nome": "Exam Name",
      "grade": 0,
      "CFU": 0,
      "date": "DD-MM-YYYY"
    }
  ],
  "alpha": 0,
  "cfu_off": 0,
  "anni_fuori_corso": 0
}
```

---
After having created the configuration file, run the script. Then, it is possible to:

1. **Add Exam** - Select option `1` Register the result of an exam, by inserting _grade_ and _date_.

2. **Remove Exam** - Select option `2` Remove an already registered exam. It is necessary to remove the exam to
   eventually edit it.

3. **Compute Starting Grade**:
    - Select option `3` to compute the starting grade for graduation.
    - The script will display the weighted average and the starting grade.

4. **Reset Exams** - Select option `4` to reset all exams. Grades will be set to 0, while dates to `null`.

5. **Simulate Exam** - Select option `5` to simulate the impact of a single grade over the average and the starting
   grade.

## License

This project is licensed under the MIT License.
