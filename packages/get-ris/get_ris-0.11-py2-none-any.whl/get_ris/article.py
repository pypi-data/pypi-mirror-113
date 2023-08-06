class Article():
    def __init__(self,title,authors,year,type,publisher,abstract) -> None:
        self.title = title
        self.year = year
        self.type = type
        self.authors = authors
        self.publisher = publisher
        self.abstract = abstract

    def convert_to_Endnote(self):
        content = ''
        content+=f'%0 {self.type}\n'
        for author in self.authors:
            content+=f'%A {author}\n'
        content+=f'%T {self.title}\n'
        content+=f'%J {self.publisher}\n'
        content+=f'%D {self.year}\n'
        content+=f'%X {self.abstract}\n'
        return content
        
    def __repr__(self) -> str:
        return self.convert_to_Endnote()