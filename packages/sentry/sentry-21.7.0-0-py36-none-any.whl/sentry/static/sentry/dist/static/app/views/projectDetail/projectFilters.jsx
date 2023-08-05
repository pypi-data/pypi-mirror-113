Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var smartSearchBar_1 = tslib_1.__importDefault(require("app/components/smartSearchBar"));
var locale_1 = require("app/locale");
var supportedTags = {
    'release.version': {
        key: 'release.version',
        name: 'release.version',
    },
    'release.build': {
        key: 'release.build',
        name: 'release.build',
    },
    'release.package': {
        key: 'release.package',
        name: 'release.package',
    },
    release: {
        key: 'release',
        name: 'release',
    },
};
function ProjectFilters(_a) {
    var _this = this;
    var query = _a.query, tagValueLoader = _a.tagValueLoader, onSearch = _a.onSearch;
    var getTagValues = function (tag, currentQuery) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
        var values;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, tagValueLoader(tag.key, currentQuery)];
                case 1:
                    values = _a.sent();
                    return [2 /*return*/, values.map(function (_a) {
                            var value = _a.value;
                            return value;
                        })];
            }
        });
    }); };
    return (<smartSearchBar_1.default searchSource="project_filters" query={query} placeholder={locale_1.t('Search by release version')} maxSearchItems={5} hasRecentSearches={false} supportedTags={supportedTags} onSearch={onSearch} onGetTagValues={getTagValues}/>);
}
exports.default = ProjectFilters;
//# sourceMappingURL=projectFilters.jsx.map