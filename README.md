# andmatrix
Given a CSV file and two columns in that file, a new CSV file is output containing a matrix showing the relationship between the values in the first column and the values in the second.

For example, given the following CSV table:

|   | Species | Location ID | Count |
|---|---------|-------------|-------|
| 1 | Horse   | 1           | 209   |
| 2 | Horse   | 2           | 10    |
| 3 | Horse   | 3           | 201   |
| 4 | Cow     | 1           | 150   |
| 5 | Cow     | 2           | 900   |
| 6 | Cow     | 3           | 5     |

Selecting "Species" and "Count" as the first and second column, respectively, would produce the following output table:

|   | Count | Horse | Cow |
|---|-------|-------|-----|
| 1 | 200   | 1     | 0   |
| 2 | 10    | 1     | 0   |
| 3 | 201   | 1     | 0   |
| 4 | 150   | 0     | 1   |
| 5 | 900   | 0     | 1   |
| 6 | 5     | 0     | 1   |


