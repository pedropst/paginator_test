class Paginator:
    """
    This class is responsable to describe over the attribute message how
    a paginator should be like following the current_page, total_page,
    boundaries and around.
    
    Attributes:
        currente_page (int): Indicates where the paginator is currently located;
        total_pages (int): Indicates how many pages the paginator has;
        boundaries (int): Indicates how many pages should be unhide in the 
            beginning and ending of the paginator;
        around (int): Indicates how many pages shoud be unhide around the current 
            page;
    """
    def __init__(self, current_page: int, total_pages: int, boundaries: int, around:int) -> None:
        """
        Initializes the Paginator object and determine the paginator description.
        
        Parameters:
            currente_page (int): Indicates where the paginator is currently 
                located;
            total_pages (int): Indicates how many pages the paginator has;
            boundaries (int): Indicates how many pages should be unhide in the 
                beginning and ending of the paginator;
            around (int): Indicates how many pages shoud be unhide around the 
                current page;
        """
        self.current_page = current_page
        self.total_pages = total_pages
        self.boundary_size = boundaries
        self.around_size = around

        self.validating_parameters_types()
        self.validating_parameters_values()

        self.aroundd = self.define_pagination()
        

    def validating_parameters_types(self):
        """
        This method is responsable to verify in any parameter is not an int type.
        """

        if set(map(type, [self.current_page, self.total_pages, 
                          self.boundary_size, self.around_size])) != set([int]):
            raise TypeError('At least one parameter type is not supported. All parameters should be int.')

    def validating_parameters_values(self):
        """
        This method is responsable to keeping the boundary_size and
        around_size between the maximum interval of total pages.
        """

        if self.total_pages < 1 or self.total_pages > 2**63:
            raise ValueError('Total page is out of the positive range of 64bits.')
        if self.boundary_size < 0 or self.boundary_size > self.total_pages:
            raise ValueError('Boundary size is out of the maximum total pages range.')
        if self.around_size  < 0 or self.around_size > self.total_pages:
            raise ValueError('Around size is out of the maximum total pages range.')
        if self.current_page < 1 or self.current_page > self.total_pages:
            raise ValueError('Current page position is out of the maximum total pages range.')
        
    def define_pagination(self):
        total_boundaries_size = self.boundary_size * 2
        total_around_size = self.around_size * 2

        if total_boundaries_size >= self.total_pages:
            self.early_return = True
            self.message = ' '.join(map(str, range(1, self.total_pages + 1)))
            return
    
        if total_around_size >= self.total_pages*2:
            self.early_return = True
            self.message = ' '.join(map(str, range(1, self.total_pages + 1)))
            return
        
        if total_boundaries_size + total_around_size >= self.total_pages:
            self.early_return = True
            self.message = ' '.join(map(str, range(1, self.total_pages + 1)))
            return
        
        if total_boundaries_size + self.around_size > self.total_pages:
            self.early_return = True
            self.message = ' '.join(map(str, range(1, self.total_pages + 1)))
            return
        
        self.message = []
        self.aroundd = self.define_around()

        if not self.boundary_size and (self.current_page != 1 | self.total_pages):
            self.message += ['...']

        self.boundaries, left_boundary, right_boundary = self.define_boundaries()

        left_boundary = list(range(1, left_boundary))
        right_boundary = list(range(right_boundary + 1, self.total_pages + 1))

        self.message += left_boundary

        if 1 + self.boundary_size < self.aroundd[0] and self.message and self.message[-1] != '...':
            self.message += ['...']

        if not set(self.aroundd).issubset(right_boundary) and not set(self.aroundd).issubset(left_boundary):
            self.message += set(self.aroundd).difference(left_boundary)

        if self.aroundd[-1] < self.total_pages - self.boundary_size and self.message[-1] != '...': #TODO: PROBABLY THIS NOT GONNA WORK, MUST TEST IF THE SUM IS IN THE AROUND LIST AND GET THE INDEX
            self.message += ['...']

        if not set(right_boundary).issubset(self.aroundd):
            self.message += right_boundary

        # self.message = ' '.join(map(str, self.message))

    def define_around(self):
        if not self.around_size:
            self.early_return = True
            self.around = []
            return [self.current_page]
        
        left_around = self.current_page - self.around_size
        right_around = self.current_page + self.around_size

        if left_around < 1:
            left_around = 1
        if right_around > self.total_pages:
            right_around = self.total_pages

        self.around = list(range(left_around, right_around + 1))
        self.around.remove(self.current_page)

        return range(left_around, right_around + 1)
    
    def define_boundaries(self):
        if not self.boundary_size:
            self.early_return = True
            return [], 0, self.total_pages + 1
        
        left_boundary = 1 + self.boundary_size
        right_boundary = self.total_pages - self.boundary_size

        if left_boundary > self.total_pages:
            left_boundary = self.total_pages
        if right_boundary < 1:
            right_boundary = 1

        return range(left_boundary, right_boundary + 1), left_boundary, right_boundary
    
        
    