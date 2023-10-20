# ***************************************************************************
# *   Copyright (c) 2015 Paul Ebbers paul.ebbers@gmail.com                  *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Lesser General Public License for more details.                   *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with FreeCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************/


# This macro fills the titleblock with all the date from the spreadsheet.
# The spreadsheet is generated by the macro "PopulateSpreadsheet".
# The data in spreadsheet can be changed by the user as long the data in column A remains unchanged.
# there a multiple senarios for using these macro's:
#  - When changing the template for an different size, you can quickly refill the titleblock.
#    Of course, the editable text in the new template must be equal.
#  - Link the date to model properties like parameters. Basicly all what is achievable with the Spreadsheet workbench
#  - Import data from excel or libre office
#  - Etc.

import FreeCAD as App
import Standard_Functions


def FillTitleBlock():
    # Preset the value for the multiplier. This is used if an value has to be increased for every page.
    NumCounter = -1

    # Get the pages and go throug them one by one.
    try:
        pages = App.ActiveDocument.findObjects("TechDraw::DrawPage")
        for page in pages:
            # Get the editable texts
            texts = page.Template.EditableTexts
            # Fill the titleblock with the data from the spreadsheet named "Title block".
            # If the spreadsheet doesn't exist raise an error in the report view.
            try:
                # Get the spreadsheet.
                sheet = App.ActiveDocument.getObject("TitleBlock")

                # Increase the NumCounter
                NumCounter = NumCounter + 1

                # Go through the spreadsheet.
                for RowNum in range(1000):
                    # Start with x+1 first, to make sure that x is at least 1.
                    RowNum = RowNum + 2

                    # fill in the editable text based on the text name in column A and the value in column B.
                    try:
                        # check if there is a value. If there is an value, fill in. If not, clear the editable text.
                        str(sheet.get("B" + str(RowNum)))
                    except Exception:
                        texts[str(sheet.get("A" + str(RowNum)))] = ""
                    else:
                        if (str(sheet.get("C" + str(RowNum))).lower()).startswith("y"):
                            try:
                                (
                                    isinstance(
                                        int(str(sheet.get("B" + str(RowNum)))), int
                                    )
                                )
                                texts[str(sheet.get("A" + str(RowNum)))] = str(
                                    int(str(sheet.get("B" + str(RowNum)))) + NumCounter
                                )
                            except Exception:
                                texts[str(sheet.get("A" + str(RowNum)))] = str(
                                    sheet.get("B" + str(RowNum))
                                )
                                raise ("this is not a number!")
                        else:
                            texts[str(sheet.get("A" + str(RowNum)))] = str(
                                sheet.get("B" + str(RowNum))
                            )

                    # Check if the next row exits. If not this is the end of all the available values.
                    try:
                        sheet.get("A" + str(RowNum + 1))
                    except Exception:
                        # print("end of range")
                        break

                # Write all the updated text to the page.
                page.Template.EditableTexts = texts

            except Exception as e:
                # raise an exeception if there is no spreadsheet.
                Standard_Functions.Mbox("No spreadsheet named 'TitleBlock'!!!", "", 0)
                raise (e)

    except Exception as e:
        # raise an exeception if there is no page.
        Standard_Functions.Mbox("No page present!!!", "", 0)
        raise (e)
