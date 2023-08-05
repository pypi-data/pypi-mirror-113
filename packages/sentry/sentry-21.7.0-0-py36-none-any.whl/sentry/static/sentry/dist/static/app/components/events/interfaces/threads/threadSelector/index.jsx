Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var partition_1 = tslib_1.__importDefault(require("lodash/partition"));
var dropdownAutoComplete_1 = tslib_1.__importDefault(require("app/components/dropdownAutoComplete"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var locale_1 = require("app/locale");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var filterThreadInfo_1 = tslib_1.__importDefault(require("./filterThreadInfo"));
var header_1 = tslib_1.__importDefault(require("./header"));
var option_1 = tslib_1.__importDefault(require("./option"));
var selectedOption_1 = tslib_1.__importDefault(require("./selectedOption"));
var DROPDOWN_MAX_HEIGHT = 400;
var ThreadSelector = function (_a) {
    var threads = _a.threads, event = _a.event, exception = _a.exception, activeThread = _a.activeThread, onChange = _a.onChange;
    var getDropDownItem = function (thread) {
        var _a = filterThreadInfo_1.default(event, thread, exception), label = _a.label, filename = _a.filename, crashedInfo = _a.crashedInfo;
        var threadInfo = { label: label, filename: filename };
        return {
            value: "#" + thread.id + ": " + thread.name + " " + label + " " + filename,
            threadInfo: threadInfo,
            thread: thread,
            label: (<option_1.default id={thread.id} details={threadInfo} name={thread.name} crashed={thread.crashed} crashedInfo={crashedInfo}/>),
        };
    };
    var getItems = function () {
        var _a = tslib_1.__read(partition_1.default(threads, function (thread) { return !!(thread === null || thread === void 0 ? void 0 : thread.crashed); }), 2), crashed = _a[0], notCrashed = _a[1];
        return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(crashed)), tslib_1.__read(notCrashed)).map(getDropDownItem);
    };
    var handleChange = function (thread) {
        if (onChange) {
            onChange(thread);
        }
    };
    return (<StyledDropdownAutoComplete items={getItems()} onSelect={function (item) {
            handleChange(item.thread);
        }} maxHeight={DROPDOWN_MAX_HEIGHT} searchPlaceholder={locale_1.t('Filter Threads')} emptyMessage={locale_1.t('You have no threads')} noResultsMessage={locale_1.t('No threads found')} menuHeader={<header_1.default />} closeOnSelect emptyHidesInput>
      {function (_a) {
            var isOpen = _a.isOpen, selectedItem = _a.selectedItem;
            return (<StyledDropdownButton size="small" isOpen={isOpen} align="left">
          {selectedItem ? (<selectedOption_1.default id={selectedItem.thread.id} details={selectedItem.threadInfo}/>) : (<selectedOption_1.default id={activeThread.id} details={filterThreadInfo_1.default(event, activeThread, exception)}/>)}
        </StyledDropdownButton>);
        }}
    </StyledDropdownAutoComplete>);
};
exports.default = ThreadSelector;
var StyledDropdownAutoComplete = styled_1.default(dropdownAutoComplete_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  min-width: 300px;\n  @media (min-width: ", ") {\n    width: 500px;\n  }\n  @media (max-width: ", ") {\n    top: calc(100% - 2px);\n  }\n"], ["\n  width: 100%;\n  min-width: 300px;\n  @media (min-width: ", ") {\n    width: 500px;\n  }\n  @media (max-width: ", ") {\n    top: calc(100% - 2px);\n  }\n"])), theme_1.default.breakpoints[0], function (p) { return p.theme.breakpoints[2]; });
var StyledDropdownButton = styled_1.default(dropdownButton_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  > *:first-child {\n    grid-template-columns: 1fr 15px;\n  }\n  width: 100%;\n  min-width: 150px;\n  @media (min-width: ", ") {\n    max-width: 420px;\n  }\n"], ["\n  > *:first-child {\n    grid-template-columns: 1fr 15px;\n  }\n  width: 100%;\n  min-width: 150px;\n  @media (min-width: ", ") {\n    max-width: 420px;\n  }\n"])), function (props) { return props.theme.breakpoints[3]; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map