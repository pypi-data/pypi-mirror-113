Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var iconWarning_1 = require("app/icons/iconWarning");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var breadcrumbs_1 = require("app/types/breadcrumbs");
var event_1 = require("app/types/event");
var utils_1 = require("app/utils");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var searchBarAction_1 = tslib_1.__importDefault(require("../searchBarAction"));
var searchBarActionFilter_1 = tslib_1.__importDefault(require("../searchBarAction/searchBarActionFilter"));
var icon_1 = tslib_1.__importDefault(require("./icon"));
var level_1 = tslib_1.__importDefault(require("./level"));
var list_1 = tslib_1.__importDefault(require("./list"));
var styles_1 = require("./styles");
var utils_2 = require("./utils");
var Breadcrumbs = /** @class */ (function (_super) {
    tslib_1.__extends(Breadcrumbs, _super);
    function Breadcrumbs() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchTerm: '',
            breadcrumbs: [],
            filteredByFilter: [],
            filteredBySearch: [],
            filterOptions: {},
            displayRelativeTime: false,
        };
        _this.handleSearch = function (value) {
            _this.setState(function (prevState) { return ({
                searchTerm: value,
                filteredBySearch: _this.filterBySearch(value, prevState.filteredByFilter),
            }); });
        };
        _this.handleFilter = function (filterOptions) {
            var filteredByFilter = _this.getFilteredCrumbsByFilter(filterOptions);
            _this.setState(function (prevState) { return ({
                filterOptions: filterOptions,
                filteredByFilter: filteredByFilter,
                filteredBySearch: _this.filterBySearch(prevState.searchTerm, filteredByFilter),
            }); });
        };
        _this.handleSwitchTimeFormat = function () {
            _this.setState(function (prevState) { return ({
                displayRelativeTime: !prevState.displayRelativeTime,
            }); });
        };
        _this.handleCleanSearch = function () {
            _this.setState({ searchTerm: '' });
        };
        _this.handleResetFilter = function () {
            _this.setState(function (_a) {
                var breadcrumbs = _a.breadcrumbs, filterOptions = _a.filterOptions, searchTerm = _a.searchTerm;
                return ({
                    filteredByFilter: breadcrumbs,
                    filterOptions: Object.keys(filterOptions).reduce(function (accumulator, currentValue) {
                        accumulator[currentValue] = filterOptions[currentValue].map(function (filterOption) { return (tslib_1.__assign(tslib_1.__assign({}, filterOption), { isChecked: false })); });
                        return accumulator;
                    }, {}),
                    filteredBySearch: _this.filterBySearch(searchTerm, breadcrumbs),
                });
            });
        };
        _this.handleResetSearchBar = function () {
            _this.setState(function (prevState) { return ({
                searchTerm: '',
                filteredBySearch: prevState.breadcrumbs,
            }); });
        };
        return _this;
    }
    Breadcrumbs.prototype.componentDidMount = function () {
        this.loadBreadcrumbs();
    };
    Breadcrumbs.prototype.loadBreadcrumbs = function () {
        var _a;
        var data = this.props.data;
        var breadcrumbs = data.values;
        // Add the (virtual) breadcrumb based on the error or message event if possible.
        var virtualCrumb = this.getVirtualCrumb();
        if (virtualCrumb) {
            breadcrumbs = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(breadcrumbs)), [virtualCrumb]);
        }
        var transformedCrumbs = utils_2.transformCrumbs(breadcrumbs);
        var filterOptions = this.getFilterOptions(transformedCrumbs);
        this.setState({
            relativeTime: (_a = transformedCrumbs[transformedCrumbs.length - 1]) === null || _a === void 0 ? void 0 : _a.timestamp,
            breadcrumbs: transformedCrumbs,
            filteredByFilter: transformedCrumbs,
            filteredBySearch: transformedCrumbs,
            filterOptions: filterOptions,
        });
    };
    Breadcrumbs.prototype.getFilterOptions = function (breadcrumbs) {
        var types = this.getFilterTypes(breadcrumbs);
        var levels = this.getFilterLevels(types);
        var options = {};
        if (!!types.length) {
            options[locale_1.t('Types')] = types.map(function (type) { return omit_1.default(type, 'levels'); });
        }
        if (!!levels.length) {
            options[locale_1.t('Levels')] = levels;
        }
        return options;
    };
    Breadcrumbs.prototype.getFilterTypes = function (breadcrumbs) {
        var filterTypes = [];
        var _loop_1 = function (index) {
            var breadcrumb = breadcrumbs[index];
            var foundFilterType = filterTypes.findIndex(function (f) { return f.id === breadcrumb.type; });
            if (foundFilterType === -1) {
                filterTypes.push({
                    id: breadcrumb.type,
                    symbol: <icon_1.default {...omit_1.default(breadcrumb, 'description')} size="xs"/>,
                    isChecked: false,
                    description: breadcrumb.description,
                    levels: (breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.level) ? [breadcrumb.level] : [],
                });
                return "continue";
            }
            if ((breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.level) &&
                !filterTypes[foundFilterType].levels.includes(breadcrumb.level)) {
                filterTypes[foundFilterType].levels.push(breadcrumb.level);
            }
        };
        for (var index in breadcrumbs) {
            _loop_1(index);
        }
        return filterTypes;
    };
    Breadcrumbs.prototype.getFilterLevels = function (types) {
        var filterLevels = [];
        for (var indexType in types) {
            var _loop_2 = function (indexLevel) {
                var level = types[indexType].levels[indexLevel];
                if (filterLevels.some(function (f) { return f.id === level; })) {
                    return "continue";
                }
                filterLevels.push({
                    id: level,
                    symbol: <level_1.default level={level}/>,
                    isChecked: false,
                });
            };
            for (var indexLevel in types[indexType].levels) {
                _loop_2(indexLevel);
            }
        }
        return filterLevels;
    };
    Breadcrumbs.prototype.moduleToCategory = function (module) {
        if (!module) {
            return undefined;
        }
        var match = module.match(/^.*\/(.*?)(:\d+)/);
        if (!match) {
            return module.split(/./)[0];
        }
        return match[1];
    };
    Breadcrumbs.prototype.getVirtualCrumb = function () {
        var event = this.props.event;
        var exception = event.entries.find(function (entry) { return entry.type === event_1.EntryType.EXCEPTION; });
        if (!exception && !event.message) {
            return undefined;
        }
        var timestamp = event.dateCreated;
        if (exception) {
            var _a = exception.data.values[0], type = _a.type, value = _a.value, mdl = _a.module;
            return {
                type: breadcrumbs_1.BreadcrumbType.ERROR,
                level: breadcrumbs_1.BreadcrumbLevelType.ERROR,
                category: this.moduleToCategory(mdl) || 'exception',
                data: {
                    type: type,
                    value: value,
                },
                timestamp: timestamp,
            };
        }
        var levelTag = (event.tags || []).find(function (tag) { return tag.key === 'level'; });
        return {
            type: breadcrumbs_1.BreadcrumbType.INFO,
            level: (levelTag === null || levelTag === void 0 ? void 0 : levelTag.value) || breadcrumbs_1.BreadcrumbLevelType.UNDEFINED,
            category: 'message',
            message: event.message,
            timestamp: timestamp,
        };
    };
    Breadcrumbs.prototype.filterBySearch = function (searchTerm, breadcrumbs) {
        if (!searchTerm.trim()) {
            return breadcrumbs;
        }
        // Slightly hacky, but it works
        // the string is being `stringfy`d here in order to match exactly the same `stringfy`d string of the loop
        var searchFor = JSON.stringify(searchTerm)
            // it replaces double backslash generate by JSON.stringfy with single backslash
            .replace(/((^")|("$))/g, '')
            .toLocaleLowerCase();
        return breadcrumbs.filter(function (obj) {
            return Object.keys(pick_1.default(obj, ['type', 'category', 'message', 'level', 'timestamp', 'data'])).some(function (key) {
                var info = obj[key];
                if (!utils_1.defined(info) || !String(info).trim()) {
                    return false;
                }
                return JSON.stringify(info)
                    .replace(/((^")|("$))/g, '')
                    .toLocaleLowerCase()
                    .trim()
                    .includes(searchFor);
            });
        });
    };
    Breadcrumbs.prototype.getFilteredCrumbsByFilter = function (filterOptions) {
        var checkedTypeOptions = new Set(Object.values(filterOptions)[0]
            .filter(function (filterOption) { return filterOption.isChecked; })
            .map(function (option) { return option.id; }));
        var checkedLevelOptions = new Set(Object.values(filterOptions)[1]
            .filter(function (filterOption) { return filterOption.isChecked; })
            .map(function (option) { return option.id; }));
        var breadcrumbs = this.state.breadcrumbs;
        if (!!tslib_1.__spreadArray([], tslib_1.__read(checkedTypeOptions)).length && !!tslib_1.__spreadArray([], tslib_1.__read(checkedLevelOptions)).length) {
            return breadcrumbs.filter(function (filteredCrumb) {
                return checkedTypeOptions.has(filteredCrumb.type) &&
                    checkedLevelOptions.has(filteredCrumb.level);
            });
        }
        if (!!tslib_1.__spreadArray([], tslib_1.__read(checkedTypeOptions)).length) {
            return breadcrumbs.filter(function (filteredCrumb) {
                return checkedTypeOptions.has(filteredCrumb.type);
            });
        }
        if (!!tslib_1.__spreadArray([], tslib_1.__read(checkedLevelOptions)).length) {
            return breadcrumbs.filter(function (filteredCrumb) {
                return checkedLevelOptions.has(filteredCrumb.level);
            });
        }
        return breadcrumbs;
    };
    Breadcrumbs.prototype.getEmptyMessage = function () {
        var _a = this.state, searchTerm = _a.searchTerm, filteredBySearch = _a.filteredBySearch, filterOptions = _a.filterOptions;
        if (searchTerm && !filteredBySearch.length) {
            var hasActiveFilter = Object.values(filterOptions)
                .flatMap(function (filterOption) { return filterOption; })
                .find(function (filterOption) { return filterOption.isChecked; });
            return (<StyledEmptyMessage icon={<iconWarning_1.IconWarning size="xl"/>} action={hasActiveFilter ? (<button_1.default onClick={this.handleResetFilter} priority="primary">
                {locale_1.t('Reset filter')}
              </button_1.default>) : (<button_1.default onClick={this.handleResetSearchBar} priority="primary">
                {locale_1.t('Clear search bar')}
              </button_1.default>)}>
          {locale_1.t('Sorry, no breadcrumbs match your search query')}
        </StyledEmptyMessage>);
        }
        return (<StyledEmptyMessage icon={<iconWarning_1.IconWarning size="xl"/>}>
        {locale_1.t('There are no breadcrumbs to be displayed')}
      </StyledEmptyMessage>);
    };
    Breadcrumbs.prototype.render = function () {
        var _a = this.props, type = _a.type, event = _a.event, organization = _a.organization;
        var _b = this.state, filterOptions = _b.filterOptions, searchTerm = _b.searchTerm, filteredBySearch = _b.filteredBySearch, displayRelativeTime = _b.displayRelativeTime, relativeTime = _b.relativeTime;
        return (<StyledEventDataSection type={type} title={<guideAnchor_1.default target="breadcrumbs" position="right">
            <h3>{locale_1.t('Breadcrumbs')}</h3>
          </guideAnchor_1.default>} actions={<StyledSearchBarAction placeholder={locale_1.t('Search breadcrumbs')} onChange={this.handleSearch} query={searchTerm} filter={<searchBarActionFilter_1.default onChange={this.handleFilter} options={filterOptions}/>}/>} wrapTitle={false} isCentered>
        {!!filteredBySearch.length ? (<errorBoundary_1.default>
            <list_1.default breadcrumbs={filteredBySearch} event={event} orgId={organization.slug} onSwitchTimeFormat={this.handleSwitchTimeFormat} displayRelativeTime={displayRelativeTime} searchTerm={searchTerm} relativeTime={relativeTime} // relativeTime has to be always available, as the last item timestamp is the event created time
            />
          </errorBoundary_1.default>) : (this.getEmptyMessage())}
      </StyledEventDataSection>);
    };
    return Breadcrumbs;
}(React.Component));
exports.default = Breadcrumbs;
var StyledEventDataSection = styled_1.default(eventDataSection_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(3));
var StyledEmptyMessage = styled_1.default(emptyMessage_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), styles_1.aroundContentStyle);
var StyledSearchBarAction = styled_1.default(searchBarAction_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  z-index: 2;\n"], ["\n  z-index: 2;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map