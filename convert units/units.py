"""
=================================================================
 original written by:   James Lockley, ABAQUS UK, Jan 2005
 modified by:   Cheng JIN, China, Jan 2023

 describes the conversion of units from one measurement unit to another
 according to the formula given
 
e.g. 'K': {'C': 'x-273'}   Temperature: Celsius --> Kelvin 


 
================================================================="""


properties={}

properties['Temperature']={'F': {'C': '5./9.*(x-32)',
                                 'K': '5./9.*(x-32)+273'
                                 },
                           
                           'C': {'F': 'x*9./5.+32',
                                 'K': 'x+273'
                                 },
                           
                           'K': {'C': 'x-273',
                                 'F': '(x-273)*9./5.+32'
                                 }
                           }

properties['Mass'] = {'g':  {'kg' :  'x/1000.',
                             'ton':  'x/1e6',
                             'lb' :  'x*0.00220462262'
                             },
                      
                      'kg': {'g'  :  'x*1000.',
                             'ton':  'x/1000.',
                             'lb' :  'x*2.20462262'
                             }, 
                      
                      'lb': {'kg' :  'x/2.20462262',
                             'ton':  'x/2204.62262',
                             'g'  :  '1000*x/2.20462262'
                             }
                      }
                           


properties['Conductivity'] = {'W/(m*K)' : {'mW/(mm*K)' : 'x*1'},
                      'mW/(mm*K)': {'W/(m*K)'  : 'x*1'}
                      }

properties['Specific Heat'] = {'J/(kg*K)' : {'mJ/(ton*K)' : 'x*1e6'},
                      'mJ/(ton*K)': {'J/(kg*K)'  : 'x*1e-6'}
                      }

properties['Latent Heat'] = {'J/kg' : {'mJ/ton' : 'x*1e6'},
                      'mJ/ton': {'J/kg'  : 'x*1e-6'}
                      }

properties['Film Coefficient'] = {'J/(m^2*K^4)' : {'mJ/(mm^2*K^4)' : 'x*1e-3'},
                      'mJ/(mm^2*K^4)': {'J/(m^2*K^4)'  : 'x*1e3'}
                      }

properties['Stefan Boltzmann'] = {'W/(m^2*K*s)' : {'mW/(mm^2*K*s)' : 'x*1e-3'},
                      'mJ/(mm^2*K*s)': {'J/(m^2*K*s)'  : 'x*1e3'}
                      }

properties['E/Stress'] = {'Pa' : {'MPa' : 'x*1e-6'},
                      'MPa': {'Pa'  : 'x*1e6'}
                      }

properties['Density'] = {'kg/m^3' : {'ton/mm^3' : 'x*1e-12',
                         'g/cm^3' :'x*1e-3'},
                      'ton/mm^3': {'kg/m^3'  : 'x*1e12',
                         'g/cm^3' :'x*1e9'},
                      'g/cm^3' : {'kg/m^3' : 'x*1e-3',
                          'ton/mm^3': 'x*1e-9'}
                      }

properties['Length'] = {'mm':{'m':'x/1000.',
                              'inch': 'x/25.4',
                              'ft': 'x/304.8'},
                        'm': {'mm':'x*1000.',
                              'inch': 'x/0.0254',
                              'ft': 'x/0.3048'},
                        'inch':{'mm':'x*25.4',
                                'm':'x*25.4/1000.',
                                'ft': 'x/12.'},
                        'ft': {'mm':'x*304.8',
                                'm':'x*0.3048',
                                'inch': 'x*12.'}
                      }



if __name__ == '__main__':
    try:
        print properties
    except:
        print 'Units.py has not been imported.  Please check the syntax'
