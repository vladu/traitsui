#------------------------------------------------------------------------------
#
#  Copyright (c) 2005, Enthought, Inc.
#  All rights reserved.
#  
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#  Thanks for using Enthought open source!
#  
#  Author: David C. Morrill
#  Date:   10/14/2004
#
#------------------------------------------------------------------------------

""" Defines common traits used within the traits.ui package.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasStrictTraits, Trait, TraitPrefixList, Delegate, Str, Instance, \
           List, Enum, Any, Range, Expression, TraitType
           
from enthought.traits.trait_base \
    import get_resource_path

#-------------------------------------------------------------------------------
#  Trait definitions:
#-------------------------------------------------------------------------------

# Styles for user interface elements:
style_trait = Trait( 'simple',
                     TraitPrefixList( 'simple', 'custom', 'text', 'readonly' ),
                     cols = 4 )
                     
# Trait for the default object being edited:                     
object_trait = Expression( 'object' )                     

# The default dock style to use:
dock_style_trait = Enum( 'fixed', 'horizontal', 'vertical', 'tab',
                         desc = "the default docking style to use" )
                         
# The default notebook tab image to use:                      
image_trait = Instance( 'enthought.pyface.image_resource.ImageResource',
                        desc = 'the image to be displayed on notebook tabs' )
                     
# The category of elements dragged out of the view:
export_trait = Str( desc = 'the category of elements dragged out of the view' )

# Delegate a trait value to the object's **container** trait:                  
container_delegate = Delegate( 'container' )

# An identifier for the external help context:
help_id_trait = Str( desc = "the external help context identifier" )                     

# A button to add to a view:
a_button = Trait( '', Str, Instance( 'enthought.traits.ui.menu.Action' ) )

# The set of buttons to add to the view:
buttons_trait = List( a_button,
                      desc = 'the action buttons to add to the bottom of '
                             'the view' )

# View trait specified by name or instance:
AView = Any
#AView = Trait( '', Str, Instance( 'enthought.traits.ui.View' ) )

#-------------------------------------------------------------------------------
#  'Image' trait:
#-------------------------------------------------------------------------------

def convert_image ( value, level = 3 ):
    """ Converts a specified value to an ImageResource if possible.
    """
    from enthought.pyface.image_resource import ImageResource
    
    if isinstance( value, basestring ):
        if value[:1] == '@':
            value = ImageResource( value[1:], 
                        search_path = [ get_resource_path( 1 ) ] )
        else:   
            value = ImageResource( value,
                        search_path = [ get_resource_path( level ) ] )
                              
    return value
    
class Image ( TraitType ):
    """ Defines a trait whose value must be a PyFace ImageResource or a string
        that can be converted to one.
    """
    
    # Define the default value for the trait:
    default_value = None
    
    # A description of the type of value this trait accepts:
    info_text = 'an ImageResource or string that can be used to define one'
    
    def __init__ ( self, value = None, **metadata ):
        """ Creates an Image trait.

        Parameters
        ----------
        value : string or ImageResource
            The default value for the Image, either an ImageResource object,
            or a string from which an ImageResource object can be derived.
        """
        super( Image, self ).__init__( convert_image( value ), **metadata )

    def validate ( self, object, name, value ):
        """ Validates that a specified value is valid for this trait.
        """
        from enthought.pyface.image_resource import ImageResource
        
        value = convert_image( value, 4 )
        if (value is None) or isinstance( value, ImageResource ):
            return value
            
        self.error( object, name, value )
        
#-------------------------------------------------------------------------------
#  'Padding' class:  
#-------------------------------------------------------------------------------
                
class Padding ( HasStrictTraits ):
    
    # The amount of padding/margin at the top:
    top = Range( -32, 32, 0 )
    
    # The amount of padding/margin at the bottom:
    bottom = Range( -32, 32, 0 )
    
    # The amount of padding/margin on the left:
    left = Range( -32, 32, 0 )
    
    # The amount of padding/margin on the right:
    right = Range( -32, 32, 0 )
    
    def __init__ ( self, value = None, **traits ):
        """ Initializes the object.
        """
        if value is not None:
            self.set( top  = value, bottom = value, 
                      left = value, right  = value )
                      
        super( Padding, self ).__init__( **traits )
        
Margins = Padding

#-------------------------------------------------------------------------------
#  'HasPadding' trait:
#-------------------------------------------------------------------------------

class HasPadding ( TraitType ):
    """ Defines a trait whose value must be a Padding object or an integer
        value that can be converted to one.
    """
    
    # Define the default value for the trait:
    default_value = Padding( 0 )
    
    # A description of the type of value this trait accepts:
    info_text = ('a Padding or Margin instance or an integer in the range from '
                 '0 to 32 that can be used to define one')

    def validate ( self, object, name, value ):
        """ Validates that a specified value is valid for this trait.
        """
        if isinstance( value, int ):
            try:
                value = Padding( value )
            except:
                self.error( object, name, value )
            
        if isinstance( value, Padding ):
            return value
            
        self.error( object, name, value )
        
    def get_default_value ( self ):
        """ Returns a tuple of the form: ( default_value_type, default_value )
            which describes the default value for this trait.
        """
        dv  = self.default_value
        dvt = self.default_value_type
        if dvt < 0:
            if isinstance( dv, int ):
                dv = Padding( dv )
                
            if not isinstance( dv, Padding ):
                return super( HasPadding, self ).get_default_value()
                
            self.default_value_type = dvt = 7
            dv = ( Padding, (), dv.get() )
        
        return ( dvt, dv )
        
HasMargins = HasPadding        

#-------------------------------------------------------------------------------
#  Other definitions:
#-------------------------------------------------------------------------------

# Types that represent sequences
SequenceTypes = ( tuple, list )
