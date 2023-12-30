def transform(self, x, y):  # 2D coordinates
    # return self.transform_2D(x,y)
    return self.transform_perspective(x, y)  # -- to make it easy to go to perspective mode from 2D, we hide
    # transform 2D.
    # If we show transform perspective and hide transform 2D it doesn't change anything, but interesting
    # thing is we can compute all the coordinates in 2D, just before going to the display we are going to
    # transform the coordinates.


def transform_2D(self, x, y):  # result of transform fn
    return int(x), int(y)  # using int for non-floating coordinates


# Doesn't change anything  for now interesting things is we can have another function
# Which is perspective function and let's implement it.
def transform_perspective(self, x, y):
    # Applying proportion now..
    lin_y = y * self.perspective_point_y / self.height  # self.height is the height of the window
    if lin_y > self.perspective_point_y:
        lin_y = self.perspective_point_y

    diff_x = x - self.perspective_point_x
    diff_y = self.perspective_point_y - lin_y
    factor_y = diff_y / self.perspective_point_y  # 1 when diff_y == self.perspective_point / 0 when diff_y = 0
    factor_y = pow(factor_y, 4)  # this is same as factor_y * factor_y

    tr_x = self.perspective_point_x + diff_x * factor_y
    tr_y = self.perspective_point_y - factor_y * self.perspective_point_y

    return int(tr_x), int(tr_y)
