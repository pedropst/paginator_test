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

        self.define_pagination()
        print(self.message)
        
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
        """
        This method is going to evaluate the paginator 
        allocating into self.message the paginator string.
        """
                
        self.pagination = []
        self.arounds = self.define_around()

        left_boundary, right_boundary = self.define_boundaries()
        self.boundaries = list(set(left_boundary + right_boundary))

        if self.checking_for_overflow_cases():  
            return
        
        self.pagination.extend(left_boundary)
    
        if 1 + self.boundary_size < self.arounds[0]:
            self.pagination.extend(['...'])

        if right_boundary and self.arounds and right_boundary[0] < self.arounds[0]:
            self.pagination.extend(right_boundary)
            self.message = ' '.join(map(str, self.pagination))
            return
        
        if self.arounds and self.arounds[0] in self.pagination:
            if self.pagination[-1] in self.arounds:
                index = self.arounds.index(self.pagination[-1])
                self.pagination.extend(self.arounds[index+1:])
        else:
            self.pagination.extend(self.arounds)

            if self.pagination[-1] == self.total_pages:
                self.message = ' '.join(map(str, self.pagination))
                return
        
        if (self.arounds[-1] < self.total_pages - self.boundary_size 
            and self.pagination[-1] != '...'):
            self.pagination.extend(['...'])

        self.pagination.extend(right_boundary)

        self.message = ' '.join(map(str, self.pagination))

    def define_around(self):
        """
        This method is responsable to get the arounds determinated
        by the around_size variable. It also prevents the around
        to overflow the maximum interval of total pages.
        """

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
        """
        This method is responsable to get the boundaries determinated
        by the boundary_size variable. It also prevents the boundaries
        to overflow the maximum interval of total pages.
        """

        if not self.boundary_size:
            self.early_return = True
            return [], []
        
        left_boundary = 1 + self.boundary_size
        right_boundary = self.total_pages - self.boundary_size

        if left_boundary > self.total_pages:
            left_boundary = self.total_pages
        if right_boundary < 1:
            right_boundary = 1

        return (list(range(1, left_boundary)), 
                list(range(right_boundary + 1, self.total_pages + 1)))
    
    def checking_for_overflow_cases(self):
        """
        This method is responsable to evaluate common situations where
        the boundaries and around lenght might overflows, for those 
        situations this method will provoke and early return of the 
        define_pagination method for perfomance improvement.
        """

        if len(self.boundaries) >= self.total_pages:
            self.early_return = True
            self.message = ' '.join(map(str, self.boundaries))
            return True

        if len(self.arounds) >= self.total_pages:
            self.early_return = True
            self.message = ' '.join(map(str, self.arounds))
            return True
