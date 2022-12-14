### What is this doc?

Let's use this to record the findings, decisions taken, and their justifications taken during each step of the process. Eventually, we'll compile all of this into our final report.

------

[TOC]

------

## Step 1: EDA, cleaning, encoding, normalizing

| Feature              | Findings                                                     | Cleaning step                                                | Treatment/Encoding                                           | Normalization           | Justification                                                |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------------------- | ------------------------------------------------------------ |
| listing_id           | Just an identifier                                           |                                                              | Drop the column                                              |                         | ID column                                                    |
| title                | Title of listing                                             |                                                              | Drop the column                                              |                         | All information here is also present in other columns        |
| address              | Address format varies. In some places it is block number followed by street (`7 fernvale close`), in some places just the street (`cashew road`), and sometimes just the district (`sembawang / yishun (d27)`). |                                                              | Drop the column.                                             |                         | We felt we could do better with the location afforded  by lat/long and subzone, which are consistent, specific, and granular enough. |
| property_name        | Name of the condo or HDB.                                    |                                                              | Target encode to average per sq. ft. price for the property in our database. | Standard normalization  | This is the most granular level of location detail we have. Apartments in a particular Condo/HDB should have very similar per sq.ft. prices given the same location amenities etc. Therefore, we are target encoding this. TODO: What to do when a query has a property name not present in our training set? |
| property_type        |                                                              | Everything to lower caps. Convert all `hdb n rooms` values to just `hdb`. | One hot encode the resulting set of possible property types. |                         | Property type is an important distinction for both recommendation and predicting the price of a new property. Since the category cardinality is small, we go with one hot encoding for this field. |
| tenure               | Some values are empty. Most of the values are close to either 99 year lease, 1000 year lease, or are freehold. | Approximate and reduce to three categories - `99-year lease`, `999-year lease`, and `freehold`. Try to fill `null` values by copying value from the same property name. | Drop records with null even after cleaning. One hot encode the three resulting catgories. |                         | Small cardinality plus an important value to determine prices, so one-hot makes sense. Approximating makes sense since a 94 year lease won't be very different from a 102 year lease for a buyer. |
| built_year           | Some empty values                                            | Try to fill `null` values by copying value from the same property name. | Drop records with null values. Encode rest as it is.         | Standard normalization  | Keeping built year                                           |
| num_beds             | Some empty values                                            |                                                              | Drop records with empty values. Encode as it is.             |                         | Number of bedrooms is an important attribute to determining price, so it makes sense to drop record if value not available. Small value so no need to normalize. |
| num_baths            | Some empty values                                            |                                                              | Drop records with empty values. Encode as it is.             |                         | Number of bathrooms is an important attribute to determining price, so it makes sense to drop record if value not available.  Small value so no need to normalize. |
| size_sqft            | One listing id had `0` size.                                 |                                                              | Drop the <=0 values.                                         | Standard normalization  | Area can be a large number, so normalizing to a value between 0 and 1 makes sense. |
| floor_level          | Too many missing values, with values missing across categories. |                                                              | Drop the column.                                             |                         | Not possible to fill the missing values up reasonably.       |
| furnishing           | 10 `na` values. 14K records of `unspecified` values.         | Remove records with `na` values.                             | One hot encode the furnishing value.                         |                         | Furnishing level can make a difference to the price of a property. Even though many values are unspecified, we keep this column and one hot encode it to capture the information here. |
| available_unit_types | Missing values. No standard format.                          |                                                              | Drop the column.                                             |                         | This is the types of apartments available in the building. While this may indirectly indicate how *prime* a property is, we hope the target encoding on property name and location will capture that information better. |
| total_num_units      | Missing values.                                              |                                                              | Drop the column.                                             |                         | Same logic as above for `available_unit_types`               |
| property_details_url | Just a URL for the listing.                                  |                                                              | Drop the column.                                             |                         |                                                              |
| lat and lng          | Some values outside singapore                                |                                                              | Drop records with invalid (outside SG) values.               |                         | We want the model to learn that certain locations are pricier than certain other locations. It makes sense then to target encode latitude and longitude of a property to the average price/sq. ft. of properties (in our training set) within a 1km square area centered on the property. Finally, we choose this feature if the price/sq. ft. from property_name isn't available. And in case we find there are no properties in our training set within 1km square of the property in question, we use the price/sq. ft. from subzone. (If that is not available, we use price/sq. ft. from planning_area.?) |
| elevation            | 0 for all values                                             |                                                              | Drop the column                                              |                         |                                                              |
| subzone              | Some missing values.                                         | Try to fill `null` values by copying value from the same property name. | Drop records with null even after cleaning. Target encode to average price per sq. ft. for the subzone. | Standard normalization. | Subzone is critical location data which could tell us how *prime* a location is. |
| planning_area        | Some missing values.                                         |                                                              | Drop column.                                                 |                         | Subzone is a more granular location indicator, so we are relying on that to convey the impact of lcoation on property price. Within a planning_area there may be high variance of prices per sq ft, demand, etc. |
| price                | Some values are 0.                                           | Remove records with 0/null price                             | Encode as it is.                                             | Standard normalization. |                                                              |



## Step 1.5: Data augmentation - creating new features

Ways to use lat/long to create useful features:

1. Some form of target encoding on nearby property prices per sq ft. 
   - How do we define `nearby`? Just all prices within a radius?  Or within the closest cluster?
     - We can try to get a price/sq.ft. heat map on location based on lat long. That can give us insight what kind of clustering could work.
2. One option could be to learn this price/sq ft landscape as a function of lat long given the data we have. If it is a fairly general/smooth curve, it could capture the price/sq ft as a function of location pretty well. 
   - But isn't this equivalent to leaving the lat long as it is in the dataset and run the model?
     - The relationship between lat/long and price/sq ft will necessarily be a polynomial relationship. But the relationship between property price (target) and price/sq ft based on lat/long will be linear. By pre training a polynomial model on lat/long, we can keep the final model simpler/avoid polynomial features there, since everything else there is going to be either directly or indirectly proportional to the property price.

On other aux data. We are already capturing 

1.  subzone level target price/sq ft
2.  property_name, address level target price/sq ft
3.  Label encode property type
4.  One hot encode furnishing, tenure
5.  Subtract built year from 2022

Does it then make sense to include data on schools etc in proximity to the location?

