# Grade Manager

This script is designed to help students at "Politecnico di Bari" manage their exam grades and compute their starting
grade for graduation. It provides a comprehensive set of tools for exam management and grade simulation.

## Features

- **Add Exam**: Add a new exam to the list or register a grade for an existing exam.
- **Update Exam**: Modify the grade and date of an already registered exam.
- **Remove Exam**: Remove an exam from the list.
- **Compute Starting Grade**: Calculate the starting grade for graduation based on the current exams.
- **Reset Exams**: Reset all exam grades and dates.
- **Simulate Exam**: Simulate the impact of a single grade on the overall average, without saving it.
- **Modify Parameters**: Change the configuration parameters (fuori_corso, cfu_off, alpha).
- **List All Exams**: Display all registered exams in a formatted table with summary statistics.

## Usage

The script is based on the configuration file `exams.json`, used to keep track of the exams (grade, CFU, date).
Moreover, at the end of the file there are other parameters that can be modified:

- `fuori_corso`: the number of years out of course.
- `cfu_off`: the number of CFU that can be excluded from the calculation (e.g., 9 for LM, 12 for LT).
- `alpha`: the weight of the final exam (0 - 0.08).

Regarding the `lodi` parameter, it is computed automatically by the script by counting the number of exams with a grade of 30 cum laude (i.e., `gamma`). Notice that:

- **to register a 30L, the student has to write 31**.
- **a 31 is still considered as a 30 in the average computation**.

Here it is the template of the configuration file:

```json
{
  "exams": [
    {
      "name": "Exam Name",
      "grade": 0,
      "CFU": 0,
      "date": "DD-MM-YYYY"
    }
  ],
  "alpha": 0,
  "cfu_off": 0,
  "fuori_corso": 0
}
```

---
After running the script, it will automatically create the configuration file if it doesn't exist. Then, it is possible to:

1. **Add Exam** - Select option `1` to register a new exam or add a grade to an existing exam without a grade.

2. **Update Exam** - Select option `2` to modify the grade and date of an already registered exam.

3. **Remove Exam** - Select option `3` to remove an exam from the list.

4. **Compute Starting Grade** - Select option `4` to compute the starting grade for graduation. The script will display both the regular and filtered weighted averages along with the starting grades.

5. **Reset Exams** - Select option `5` to reset all exams. Grades will be set to 0, while dates to `null`.

6. **Simulate Exam** - Select option `6` to simulate the impact of a single grade over the average and the starting grade without saving it to the file.

7. **Modify Parameters** - Select option `7` to change the configuration parameters (fuori_corso, cfu_off, alpha) interactively.

8. **List All Exams** - Select option `8` to display all registered exams in a formatted table showing completed and pending exams with summary statistics.

## License

This project is licensed under the MIT License.
