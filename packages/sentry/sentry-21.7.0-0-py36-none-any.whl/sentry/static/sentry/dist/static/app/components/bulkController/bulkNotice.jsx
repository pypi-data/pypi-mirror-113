Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var button_1 = tslib_1.__importDefault(require("../button"));
var panels_1 = require("../panels");
function getSelectAllText(allRowsCount, bulkLimit) {
    if (!utils_1.defined(allRowsCount)) {
        return {
            noticeText: locale_1.t('Selected all items across all pages.'),
            actionText: locale_1.t('Select all items across all pages.'),
        };
    }
    if (bulkLimit && allRowsCount > bulkLimit) {
        return {
            noticeText: locale_1.tct('Selected up to the first [count] items.', {
                count: bulkLimit,
            }),
            actionText: locale_1.tct('Select the first [count] items.', {
                count: bulkLimit,
            }),
        };
    }
    return {
        noticeText: locale_1.tct('Selected all [count] items.', {
            count: allRowsCount,
        }),
        actionText: locale_1.tct('Select all [count] items.', {
            count: allRowsCount,
        }),
    };
}
function BulkNotice(_a) {
    var selectedRowsCount = _a.selectedRowsCount, columnsCount = _a.columnsCount, isPageSelected = _a.isPageSelected, isAllSelected = _a.isAllSelected, onSelectAllRows = _a.onSelectAllRows, onUnselectAllRows = _a.onUnselectAllRows, bulkLimit = _a.bulkLimit, allRowsCount = _a.allRowsCount, className = _a.className;
    if ((allRowsCount && allRowsCount <= selectedRowsCount) || !isPageSelected) {
        return null;
    }
    var _b = getSelectAllText(allRowsCount, bulkLimit), noticeText = _b.noticeText, actionText = _b.actionText;
    return (<Wrapper columnsCount={columnsCount} className={className}>
      {isAllSelected ? (<React.Fragment>
          {noticeText}{' '}
          <AlertButton priority="link" onClick={onUnselectAllRows}>
            {locale_1.t('Cancel selection.')}
          </AlertButton>
        </React.Fragment>) : (<React.Fragment>
          {locale_1.tn('%s item on this page selected.', '%s items on this page selected.', selectedRowsCount)}{' '}
          <AlertButton priority="link" onClick={onSelectAllRows}>
            {actionText}
          </AlertButton>
        </React.Fragment>)}
    </Wrapper>);
}
var Wrapper = styled_1.default(function (_a) {
    var _columnsCount = _a.columnsCount, props = tslib_1.__rest(_a, ["columnsCount"]);
    return (<panels_1.PanelAlert {...props}/>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-column: span ", ";\n  text-align: center;\n"], ["\n  grid-column: span ", ";\n  text-align: center;\n"])), function (p) { return p.columnsCount; });
var AlertButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  &,\n  &:hover,\n  &:active,\n  &:focus {\n    /* match the styles of an <a> tag inside Alert */\n    color: ", ";\n    border: none;\n    border-radius: 0;\n    border-bottom: 1px dotted ", ";\n    padding-bottom: 1px;\n    font-size: 15px;\n  }\n"], ["\n  &,\n  &:hover,\n  &:active,\n  &:focus {\n    /* match the styles of an <a> tag inside Alert */\n    color: ", ";\n    border: none;\n    border-radius: 0;\n    border-bottom: 1px dotted ", ";\n    padding-bottom: 1px;\n    font-size: 15px;\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
exports.default = BulkNotice;
var templateObject_1, templateObject_2;
//# sourceMappingURL=bulkNotice.jsx.map