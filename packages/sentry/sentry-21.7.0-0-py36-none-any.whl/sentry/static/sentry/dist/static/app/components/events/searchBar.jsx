Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var assign_1 = tslib_1.__importDefault(require("lodash/assign"));
var flatten_1 = tslib_1.__importDefault(require("lodash/flatten"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var memoize_1 = tslib_1.__importDefault(require("lodash/memoize"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var tags_1 = require("app/actionCreators/tags");
var smartSearchBar_1 = tslib_1.__importDefault(require("app/components/smartSearchBar"));
var constants_1 = require("app/constants");
var types_1 = require("app/types");
var utils_1 = require("app/utils");
var fields_1 = require("app/utils/discover/fields");
var measurements_1 = tslib_1.__importDefault(require("app/utils/measurements/measurements"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withTags_1 = tslib_1.__importDefault(require("app/utils/withTags"));
var SEARCH_SPECIAL_CHARS_REGEXP = new RegExp("^" + constants_1.NEGATION_OPERATOR + "|\\" + constants_1.SEARCH_WILDCARD, 'g');
var SearchBar = /** @class */ (function (_super) {
    tslib_1.__extends(SearchBar, _super);
    function SearchBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Returns array of tag values that substring match `query`; invokes `callback`
         * with data when ready
         */
        _this.getEventFieldValues = memoize_1.default(function (tag, query, endpointParams) {
            var _a;
            var _b = _this.props, api = _b.api, organization = _b.organization, projectIds = _b.projectIds;
            var projectIdStrings = (_a = projectIds) === null || _a === void 0 ? void 0 : _a.map(String);
            if (fields_1.isAggregateField(tag.key) || fields_1.isMeasurement(tag.key)) {
                // We can't really auto suggest values for aggregate fields
                // or measurements, so we simply don't
                return Promise.resolve([]);
            }
            return tags_1.fetchTagValues(api, organization.slug, tag.key, query, projectIdStrings, endpointParams, 
            // allows searching for tags on transactions as well
            true).then(function (results) {
                return flatten_1.default(results.filter(function (_a) {
                    var name = _a.name;
                    return utils_1.defined(name);
                }).map(function (_a) {
                    var name = _a.name;
                    return name;
                }));
            }, function () {
                throw new Error('Unable to fetch event field values');
            });
        }, function (_a, query) {
            var key = _a.key;
            return key + "-" + query;
        });
        /**
         * Prepare query string (e.g. strip special characters like negation operator)
         */
        _this.prepareQuery = function (query) { return query.replace(SEARCH_SPECIAL_CHARS_REGEXP, ''); };
        return _this;
    }
    SearchBar.prototype.componentDidMount = function () {
        var _a, _b;
        // Clear memoized data on mount to make tests more consistent.
        (_b = (_a = this.getEventFieldValues.cache).clear) === null || _b === void 0 ? void 0 : _b.call(_a);
    };
    SearchBar.prototype.componentDidUpdate = function (prevProps) {
        var _a, _b;
        if (!isEqual_1.default(this.props.projectIds, prevProps.projectIds)) {
            // Clear memoized data when projects change.
            (_b = (_a = this.getEventFieldValues.cache).clear) === null || _b === void 0 ? void 0 : _b.call(_a);
        }
    };
    SearchBar.prototype.getTagList = function (measurements) {
        var _a = this.props, fields = _a.fields, organization = _a.organization, tags = _a.tags, omitTags = _a.omitTags;
        var functionTags = fields
            ? Object.fromEntries(fields
                .filter(function (item) {
                return !Object.keys(fields_1.FIELD_TAGS).includes(item.field) && !fields_1.isEquation(item.field);
            })
                .map(function (item) { return [item.field, { key: item.field, name: item.field }]; }))
            : {};
        var fieldTags = organization.features.includes('performance-view')
            ? Object.assign({}, measurements, fields_1.FIELD_TAGS, functionTags)
            : omit_1.default(fields_1.FIELD_TAGS, fields_1.TRACING_FIELDS);
        var semverTags = organization.features.includes('semver')
            ? Object.assign({}, fields_1.SEMVER_TAGS, fieldTags)
            : fieldTags;
        var combined = assign_1.default({}, tags, semverTags);
        combined.has = {
            key: 'has',
            name: 'Has property',
            values: Object.keys(combined),
            predefined: true,
        };
        return omit_1.default(combined, omitTags !== null && omitTags !== void 0 ? omitTags : []);
    };
    SearchBar.prototype.render = function () {
        var _this = this;
        var organization = this.props.organization;
        return (<measurements_1.default organization={organization}>
        {function (_a) {
                var measurements = _a.measurements;
                var tags = _this.getTagList(measurements);
                return (<react_1.ClassNames>
              {function (_a) {
                        var css = _a.css;
                        return (<smartSearchBar_1.default {..._this.props} hasRecentSearches savedSearchType={types_1.SavedSearchType.EVENT} onGetTagValues={_this.getEventFieldValues} supportedTags={tags} prepareQuery={_this.prepareQuery} excludeEnvironment dropdownClassName={css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n                    max-height: 300px;\n                    overflow-y: auto;\n                  "], ["\n                    max-height: 300px;\n                    overflow-y: auto;\n                  "])))}/>);
                    }}
            </react_1.ClassNames>);
            }}
      </measurements_1.default>);
    };
    return SearchBar;
}(React.PureComponent));
exports.default = withApi_1.default(withTags_1.default(SearchBar));
var templateObject_1;
//# sourceMappingURL=searchBar.jsx.map