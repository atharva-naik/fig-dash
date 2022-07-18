import enum
import datetime
import dataclasses
from typing import *
from datetime import date as dt
from dateutil.relativedelta import relativedelta

TODAY_MINUS_18 = dt.today()-relativedelta(years=18)
# email address class.
class PeopleAppEmailAddress:
    pass

# contact number class.
class PeopleAppContactNumber:
    pass

# address format.
class PeopleAppAddress:
    pass

# gender, sex and sexual orientation (not considering romantic attraction bicurious, aromantic etc. as I have better things to do than list separate orientations and romantic attractions ...).
class PeopleAppSex(enum.Enum):
    Male = 0
    Female = 1
    InterSex = 2

class PeopleAppGender(enum.Enum):
    CisMale = 0
    CisFemale = 1
    TransMale = 2 # AFAIK trans people want this?
    TransFemale = 3
    NonBinary = 4

class PeopleAppOrientation(enum.Enum):
    HeteroSexual = 0 # opposite sex
    HomoSexual = 1 # same sex
    BiSexual = 2 # both sexes
    PanSexual = 3 # bisexual + includes non-binary people ig?
    ASexual = 4 # no sexes
# Also what is queer exactly? Someone please define that term in a way that justifies adding it to this or some other Enum.

# race (gulp)...
class PeopleAppRace(enum.Enum):
    """
    ### Categorizing Race and Ethnicity
    url: https://www.census.gov/newsroom/blogs/random-samplings/2021/08/measuring-racial-ethnic-diversity-2020-census.html
    from POV of America ig?
    1. White.
    2. Black or African American.
    3. American Indian or Alaska Native.
    4. Asian.
    5. Latino (Latino people hate the term LatinX. Ask them what they want to be called smh)
    5. Native Hawaiian or Other Pacific Islander.
    """
    White = 0
    Black = 1
    Native = 2
    Asian = 3
    Lation = 4
    Hawaiian = 5
    Other = 6

# social media sites enum
class PeopleAppSocialType(enum.Enum):
    Twitter = 0
    Facebook = 1 
    Reddit = 2
    WhatsApp = 3
    LinkedIn = 4
    Snapchat = 5
    Tumblr = 6
    Instagram = 7
    Spotify = 8
    YouTube = 9
    TikTok = 10
    Twitch = 11
    Tinder = 12
    Bumble = 13
    Grindr = 14
    Other = 15

# social medium id.
class PeopleAppSocial:
    def __init__(self, type_: PeopleAppSocialType, **data):
        self.type = type_

    @classmethod
    def Twitter(self, id: str):
        self.id = id
        self.type = PeopleAppSocialType.Twitter

# a job item
class PeopleAppJobItem:
    pass

# an education item.
class PeopleAppEducationItem:
    pass

# profile picture.
class PeopleAppProfilePicture:
    pass

# relationship status.
class PeopleAppRelationshipStatus(enum.Enum):
    Single = 0
    Dating = 1
    Engaged = 2 # to be married
    Married = 3
    Other = 4

# Bio of a Person.
class PeopleAppPersonBio:
    def __init__(self, name: str, email_addresses: List[PeopleAppEmailAddress]=[],
                 dob: dt=TODAY_MINUS_18, addresses: List[PeopleAppAddress]=[], 
                 contact_numbers: List[PeopleAppContactNumber]=[], age: int=18, 
                 education_history: List[PeopleAppEducationItem]=[], bio: str="",
                 employment_history: List[PeopleAppJobItem]=[], job_title: str="", 
                 company: str="", pronouns: Tuple[str,str,str]=("He","Him","His"),
                 orientation: PeopleAppOrientation=PeopleAppOrientation.HeteroSexual,
                 profile_pic: PeopleAppProfilePicture=PeopleAppProfilePicture.Default(),  
                 gender: PeopleAppGender=PeopleAppGender.CisMale, comments: List[str]=[],
                 sex: PeopleAppSex=PeopleAppSex.Male, race: PeopleAppRace=PeopleAppRace.White,
                 relationship_status: PeopleAppRelationshipStatus=PeopleAppRelationshipStatus.Single,  
                 socials: List[PeopleAppSocial]=[], likes: list=[], dislikes: list=[], **other):
        self.name = name
        self.contact_numbers = contact_numbers
        self.email_addresses = email_addresses
        self.addresses = addresses
        # age/dob
        self.age = age
        self.dob = dob
        # bio text, likes and dislikes
        self.bio = bio 
        self.likes = likes
        self.dislikes = dislikes
        # woke stuff 
        self.pronouns = pronouns
        self.sex = sex
        self.gender = gender
        self.orientation = orientation
        self.race = race
        # current designation.
        self.company = company
        self.job_title = job_title
        # educational and employment histories.
        self.education_history = education_history
        self.employment_history = employment_history
        self.socials = socials # various social media links for famous platforms.
        # comments & other data.
        self.comments = comments
        self.other_data = other
