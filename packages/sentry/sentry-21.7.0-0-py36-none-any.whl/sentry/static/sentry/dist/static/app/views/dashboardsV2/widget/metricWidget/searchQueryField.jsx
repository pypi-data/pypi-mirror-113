Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var memoize_1 = tslib_1.__importDefault(require("lodash/memoize"));
var smartSearchBar_1 = tslib_1.__importDefault(require("app/components/smartSearchBar"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var SEARCH_SPECIAL_CHARS_REGEXP = new RegExp("^" + constants_1.NEGATION_OPERATOR + "|\\" + constants_1.SEARCH_WILDCARD, 'g');
function SearchQueryField(_a) {
    var api = _a.api, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, tags = _a.tags, onSearch = _a.onSearch, onBlur = _a.onBlur;
    /**
     * Prepare query string (e.g. strip special characters like negation operator)
     */
    function prepareQuery(query) {
        return query.replace(SEARCH_SPECIAL_CHARS_REGEXP, '');
    }
    function fetchTagValues(tagKey) {
        return api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/metrics/tags/" + tagKey + "/", {
            method: 'GET',
        });
    }
    function getTagValues(tag, _query) {
        return fetchTagValues(tag.key).then(function (tagValues) { return tagValues; }, function () {
            throw new Error('Unable to fetch tag values');
        });
    }
    var supportedTags = tags.reduce(function (acc, tag) {
        acc[tag] = { key: tag, name: tag };
        return acc;
    }, {});
    return (<react_1.ClassNames>
      {function (_a) {
            var css = _a.css;
            return (<smartSearchBar_1.default placeholder={locale_1.t('Search for tag')} onGetTagValues={memoize_1.default(getTagValues, function (_a, query) {
                var key = _a.key;
                return key + "-" + query;
            })} supportedTags={supportedTags} prepareQuery={prepareQuery} onSearch={onSearch} onBlur={onBlur} useFormWrapper={false} excludeEnvironment dropdownClassName={css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n            max-height: 300px;\n            overflow-y: auto;\n          "], ["\n            max-height: 300px;\n            overflow-y: auto;\n          "])))}/>);
        }}
    </react_1.ClassNames>);
}
exports.default = SearchQueryField;
var templateObject_1;
//# sourceMappingURL=searchQueryField.jsx.map