
import odf.opendocument
import odf.table
import odf.text

class Sheet:

    def get(self, row, column):
        """Returns the data of the cell at the given coordinates"""
        r, c = -1
        s = []
        for el in self.element.getElementsByType(odf.table.TableRow):
            r += el.getAttribute("numberrowsrepeated")
            if r == row:
                r = el
                break
            elif r > row:
                return None
        else:
            return None
        for el in r.getElementsByType(odf.table.TableCell):
            c += el.getAttribute("numbercolumnsrepeated")
            if c == col:
                c = el
                break
            elif c > col:
                return None
        else:
            return None
        for el in c.childNodes:
            if el.isInstanceOf(odf.table.P):
                s.append(str(el))
        return ''.join(s)


    @property
    def name(self):
        self.element.getAttribute("name")

    @classmethod
    def from_element(cls, element):
        if not element.isInstanceOf(odf.table.Table):
            raise ValueError("element must be an ODF Table")

        new = cls.__new__(cls)
        new.element = element
        return new
