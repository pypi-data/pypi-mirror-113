Object.defineProperty(exports, "__esModule", { value: true });
exports.setRenderPrebuilt = exports.shouldRenderPrebuilt = exports.generateFieldOptions = exports.getExpandedResults = exports.downloadAsCsv = exports.getPrebuiltQueries = exports.generateTitle = exports.pushEventViewToLocation = exports.decodeColumnOrder = void 0;
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var papaparse_1 = tslib_1.__importDefault(require("papaparse"));
var gridEditable_1 = require("app/components/gridEditable");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var dates_1 = require("app/utils/dates");
var fields_1 = require("app/utils/discover/fields");
var events_1 = require("app/utils/events");
var localStorage_1 = tslib_1.__importDefault(require("app/utils/localStorage"));
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var types_1 = require("./table/types");
var data_1 = require("./data");
var TEMPLATE_TABLE_COLUMN = {
    key: '',
    name: '',
    type: 'never',
    isSortable: false,
    column: Object.freeze({ kind: 'field', field: '' }),
    width: gridEditable_1.COL_WIDTH_UNDEFINED,
};
// TODO(mark) these types are coupled to the gridEditable component types and
// I'd prefer the types to be more general purpose but that will require a second pass.
function decodeColumnOrder(fields) {
    var equations = 0;
    return fields.map(function (f) {
        var column = tslib_1.__assign({}, TEMPLATE_TABLE_COLUMN);
        var col = fields_1.explodeFieldString(f.field);
        var columnName = f.field;
        if (fields_1.isEquation(f.field)) {
            columnName = "equation[" + equations + "]";
            equations += 1;
        }
        column.key = columnName;
        column.name = columnName;
        column.width = f.width || gridEditable_1.COL_WIDTH_UNDEFINED;
        if (col.kind === 'function') {
            // Aggregations can have a strict outputType or they can inherit from their field.
            // Otherwise use the FIELDS data to infer types.
            var outputType = fields_1.aggregateFunctionOutputType(col.function[0], col.function[1]);
            if (outputType !== null) {
                column.type = outputType;
            }
            var aggregate = fields_1.AGGREGATIONS[col.function[0]];
            column.isSortable = aggregate && aggregate.isSortable;
        }
        else if (col.kind === 'field') {
            if (fields_1.FIELDS.hasOwnProperty(col.field)) {
                column.type = fields_1.FIELDS[col.field];
            }
            else if (fields_1.isMeasurement(col.field)) {
                column.type = fields_1.measurementType(col.field);
            }
            else if (fields_1.isSpanOperationBreakdownField(col.field)) {
                column.type = 'duration';
            }
        }
        column.column = col;
        return column;
    });
}
exports.decodeColumnOrder = decodeColumnOrder;
function pushEventViewToLocation(props) {
    var location = props.location, nextEventView = props.nextEventView;
    var extraQuery = props.extraQuery || {};
    var queryStringObject = nextEventView.generateQueryStringObject();
    react_router_1.browserHistory.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, extraQuery), queryStringObject) }));
}
exports.pushEventViewToLocation = pushEventViewToLocation;
function generateTitle(_a) {
    var eventView = _a.eventView, event = _a.event, organization = _a.organization;
    var titles = [locale_1.t('Discover')];
    var eventViewName = eventView.name;
    if (typeof eventViewName === 'string' && String(eventViewName).trim().length > 0) {
        titles.push(String(eventViewName).trim());
    }
    var eventTitle = event ? events_1.getTitle(event, organization === null || organization === void 0 ? void 0 : organization.features).title : undefined;
    if (eventTitle) {
        titles.push(eventTitle);
    }
    titles.reverse();
    return titles.join(' - ');
}
exports.generateTitle = generateTitle;
function getPrebuiltQueries(organization) {
    var views = tslib_1.__spreadArray([], tslib_1.__read(data_1.ALL_VIEWS));
    if (organization.features.includes('performance-view')) {
        // insert transactions queries at index 2
        views.splice.apply(views, tslib_1.__spreadArray([2, 0], tslib_1.__read(data_1.TRANSACTION_VIEWS)));
        views.push.apply(views, tslib_1.__spreadArray([], tslib_1.__read(data_1.WEB_VITALS_VIEWS)));
    }
    return views;
}
exports.getPrebuiltQueries = getPrebuiltQueries;
function disableMacros(value) {
    var unsafeCharacterRegex = /^[\=\+\-\@]/;
    if (typeof value === 'string' && ("" + value).match(unsafeCharacterRegex)) {
        return "'" + value;
    }
    return value;
}
function downloadAsCsv(tableData, columnOrder, filename) {
    var data = tableData.data;
    var headings = columnOrder.map(function (column) { return column.name; });
    var csvContent = papaparse_1.default.unparse({
        fields: headings,
        data: data.map(function (row) {
            return headings.map(function (col) {
                col = fields_1.getAggregateAlias(col);
                return disableMacros(row[col]);
            });
        }),
    });
    // Need to also manually replace # since encodeURI skips them
    var encodedDataUrl = "data:text/csv;charset=utf8," + encodeURIComponent(csvContent);
    // Create a download link then click it, this is so we can get a filename
    var link = document.createElement('a');
    var now = new Date();
    link.setAttribute('href', encodedDataUrl);
    link.setAttribute('download', filename + " " + dates_1.getUtcDateString(now) + ".csv");
    link.click();
    link.remove();
    // Make testing easier
    return encodedDataUrl;
}
exports.downloadAsCsv = downloadAsCsv;
var ALIASED_AGGREGATES_COLUMN = {
    last_seen: 'timestamp',
    failure_count: 'transaction.status',
};
/**
 * Convert an aggregate into the resulting column from a drilldown action.
 * The result is null if the drilldown results in the aggregate being removed.
 */
function drilldownAggregate(func) {
    var _a;
    var key = func.function[0];
    var aggregation = fields_1.AGGREGATIONS[key];
    var column = func.function[1];
    if (ALIASED_AGGREGATES_COLUMN.hasOwnProperty(key)) {
        // Some aggregates are just shortcuts to other aggregates with
        // predefined arguments so we can directly map them to the result.
        column = ALIASED_AGGREGATES_COLUMN[key];
    }
    else if ((_a = aggregation === null || aggregation === void 0 ? void 0 : aggregation.parameters) === null || _a === void 0 ? void 0 : _a[0]) {
        var parameter = aggregation.parameters[0];
        if (parameter.kind !== 'column') {
            // The aggregation does not accept a column as a parameter,
            // so we clear the column.
            column = '';
        }
        else if (!column && parameter.required === false) {
            // The parameter was not given for a non-required parameter,
            // so we fall back to the default.
            column = parameter.defaultValue;
        }
    }
    else {
        // The aggregation does not exist or does not have any parameters,
        // so we clear the column.
        column = '';
    }
    return column ? { kind: 'field', field: column } : null;
}
/**
 * Convert an aggregated query into one that does not have aggregates.
 * Will also apply additions conditions defined in `additionalConditions`
 * and generate conditions based on the `dataRow` parameter and the current fields
 * in the `eventView`.
 */
function getExpandedResults(eventView, additionalConditions, dataRow) {
    var fieldSet = new Set();
    // Expand any functions in the resulting column, and dedupe the result.
    // Mark any column as null to remove it.
    var expandedColumns = eventView.fields.map(function (field) {
        var exploded = fields_1.explodeFieldString(field.field);
        var column = exploded.kind === 'function' ? drilldownAggregate(exploded) : exploded;
        if (
        // if expanding the function failed
        column === null ||
            // the new column is already present
            fieldSet.has(column.field) ||
            // Skip aggregate equations, their functions will already be added so we just want to remove it
            fields_1.isAggregateEquation(field.field)) {
            return null;
        }
        fieldSet.add(column.field);
        return column;
    });
    // id should be default column when expanded results in no columns; but only if
    // the Discover query's columns is non-empty.
    // This typically occurs in Discover drilldowns.
    if (fieldSet.size === 0 && expandedColumns.length) {
        expandedColumns[0] = { kind: 'field', field: 'id' };
    }
    // update the columns according the the expansion above
    var nextView = expandedColumns.reduceRight(function (newView, column, index) {
        return column === null
            ? newView.withDeletedColumn(index, undefined)
            : newView.withUpdatedColumn(index, column, undefined);
    }, eventView.clone());
    nextView.query = generateExpandedConditions(nextView, additionalConditions, dataRow);
    return nextView;
}
exports.getExpandedResults = getExpandedResults;
/**
 * Create additional conditions based on the fields in an EventView
 * and a datarow/event
 */
function generateAdditionalConditions(eventView, dataRow) {
    var specialKeys = Object.values(globalSelectionHeader_1.URL_PARAM);
    var conditions = {};
    if (!dataRow) {
        return conditions;
    }
    eventView.fields.forEach(function (field) {
        var column = fields_1.explodeFieldString(field.field);
        // Skip aggregate fields
        if (column.kind === 'function') {
            return;
        }
        var dataKey = fields_1.getAggregateAlias(field.field);
        // Append the current field as a condition if it exists in the dataRow
        // Or is a simple key in the event. More complex deeply nested fields are
        // more challenging to get at as their location in the structure does not
        // match their name.
        if (dataRow.hasOwnProperty(dataKey)) {
            var value = dataRow[dataKey];
            if (Array.isArray(value)) {
                if (value.length > 1) {
                    conditions[column.field] = value;
                    return;
                }
                else {
                    // An array with only one value is equivalent to the value itself.
                    value = value[0];
                }
            }
            // if the value will be quoted, then do not trim it as the whitespaces
            // may be important to the query and should not be trimmed
            var shouldQuote = value === null || value === undefined
                ? false
                : /[\s\(\)\\"]/g.test(String(value).trim());
            var nextValue = value === null || value === undefined
                ? ''
                : shouldQuote
                    ? String(value)
                    : String(value).trim();
            if (fields_1.isMeasurement(column.field) && !nextValue) {
                // Do not add measurement conditions if nextValue is falsey.
                // It's expected that nextValue is a numeric value.
                return;
            }
            switch (column.field) {
                case 'timestamp':
                    // normalize the "timestamp" field to ensure the payload works
                    conditions[column.field] = dates_1.getUtcDateString(nextValue);
                    break;
                default:
                    conditions[column.field] = nextValue;
            }
        }
        // If we have an event, check tags as well.
        if (dataRow.tags && Array.isArray(dataRow.tags)) {
            var tagIndex = dataRow.tags.findIndex(function (item) { return item.key === dataKey; });
            if (tagIndex > -1) {
                var key = specialKeys.includes(column.field)
                    ? "tags[" + column.field + "]"
                    : column.field;
                var tagValue = dataRow.tags[tagIndex].value;
                conditions[key] = tagValue;
            }
        }
    });
    return conditions;
}
function generateExpandedConditions(eventView, additionalConditions, dataRow) {
    var parsedQuery = tokenizeSearch_1.tokenizeSearch(eventView.query);
    // Remove any aggregates from the search conditions.
    // otherwise, it'll lead to an invalid query result.
    for (var key in parsedQuery.tagValues) {
        var column = fields_1.explodeFieldString(key);
        if (column.kind === 'function') {
            parsedQuery.removeTag(key);
        }
    }
    var conditions = Object.assign({}, additionalConditions, generateAdditionalConditions(eventView, dataRow));
    // Add additional conditions provided and generated.
    for (var key in conditions) {
        var value = conditions[key];
        if (Array.isArray(value)) {
            parsedQuery.setTagValues(key, value);
            continue;
        }
        if (key === 'project.id') {
            eventView.project = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(eventView.project)), [parseInt(value, 10)]);
            continue;
        }
        if (key === 'environment') {
            if (!eventView.environment.includes(value)) {
                eventView.environment = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(eventView.environment)), [value]);
            }
            continue;
        }
        var column = fields_1.explodeFieldString(key);
        // Skip aggregates as they will be invalid.
        if (column.kind === 'function') {
            continue;
        }
        parsedQuery.setTagValues(key, [value]);
    }
    return parsedQuery.formatString();
}
function generateFieldOptions(_a) {
    var organization = _a.organization, tagKeys = _a.tagKeys, measurementKeys = _a.measurementKeys, spanOperationBreakdownKeys = _a.spanOperationBreakdownKeys, _b = _a.aggregations, aggregations = _b === void 0 ? fields_1.AGGREGATIONS : _b, _c = _a.fields, fields = _c === void 0 ? fields_1.FIELDS : _c;
    var fieldKeys = Object.keys(fields);
    var functions = Object.keys(aggregations);
    // Strip tracing features if the org doesn't have access.
    if (!organization.features.includes('performance-view')) {
        fieldKeys = fieldKeys.filter(function (item) { return !fields_1.TRACING_FIELDS.includes(item); });
        functions = functions.filter(function (item) { return !fields_1.TRACING_FIELDS.includes(item); });
    }
    // Feature flagged by arithmetic for now
    if (!organization.features.includes('discover-arithmetic')) {
        functions = functions.filter(function (item) { return item !== 'count_if'; });
    }
    var fieldOptions = {};
    // Index items by prefixed keys as custom tags can overlap both fields and
    // function names. Having a mapping makes finding the value objects easier
    // later as well.
    functions.forEach(function (func) {
        var ellipsis = aggregations[func].parameters.length ? '\u2026' : '';
        var parameters = aggregations[func].parameters.map(function (param) {
            var overrides = fields_1.AGGREGATIONS[func].getFieldOverrides;
            if (typeof overrides === 'undefined') {
                return param;
            }
            return tslib_1.__assign(tslib_1.__assign({}, param), overrides({ parameter: param, organization: organization }));
        });
        fieldOptions["function:" + func] = {
            label: func + "(" + ellipsis + ")",
            value: {
                kind: types_1.FieldValueKind.FUNCTION,
                meta: {
                    name: func,
                    parameters: parameters,
                },
            },
        };
    });
    fieldKeys.forEach(function (field) {
        fieldOptions["field:" + field] = {
            label: field,
            value: {
                kind: types_1.FieldValueKind.FIELD,
                meta: {
                    name: field,
                    dataType: fields[field],
                },
            },
        };
    });
    if (tagKeys !== undefined && tagKeys !== null) {
        tagKeys.forEach(function (tag) {
            var tagValue = fields.hasOwnProperty(tag) || fields_1.AGGREGATIONS.hasOwnProperty(tag)
                ? "tags[" + tag + "]"
                : tag;
            fieldOptions["tag:" + tag] = {
                label: tag,
                value: {
                    kind: types_1.FieldValueKind.TAG,
                    meta: { name: tagValue, dataType: 'string' },
                },
            };
        });
    }
    if (measurementKeys !== undefined && measurementKeys !== null) {
        measurementKeys.forEach(function (measurement) {
            fieldOptions["measurement:" + measurement] = {
                label: measurement,
                value: {
                    kind: types_1.FieldValueKind.MEASUREMENT,
                    meta: { name: measurement, dataType: fields_1.measurementType(measurement) },
                },
            };
        });
    }
    if (Array.isArray(spanOperationBreakdownKeys)) {
        spanOperationBreakdownKeys.forEach(function (breakdownField) {
            fieldOptions["span_op_breakdown:" + breakdownField] = {
                label: breakdownField,
                value: {
                    kind: types_1.FieldValueKind.BREAKDOWN,
                    meta: { name: breakdownField, dataType: 'duration' },
                },
            };
        });
    }
    return fieldOptions;
}
exports.generateFieldOptions = generateFieldOptions;
var RENDER_PREBUILT_KEY = 'discover-render-prebuilt';
function shouldRenderPrebuilt() {
    var shouldRender = localStorage_1.default.getItem(RENDER_PREBUILT_KEY);
    return shouldRender === 'true' || shouldRender === null;
}
exports.shouldRenderPrebuilt = shouldRenderPrebuilt;
function setRenderPrebuilt(value) {
    localStorage_1.default.setItem(RENDER_PREBUILT_KEY, value ? 'true' : 'false');
}
exports.setRenderPrebuilt = setRenderPrebuilt;
//# sourceMappingURL=utils.jsx.map