Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var sortBy_1 = tslib_1.__importDefault(require("lodash/sortBy"));
var contextData_1 = tslib_1.__importDefault(require("app/components/contextData"));
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var utils_1 = require("app/utils");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var KeyValueList = function (_a) {
    var data = _a.data, _b = _a.isContextData, isContextData = _b === void 0 ? false : _b, _c = _a.isSorted, isSorted = _c === void 0 ? true : _c, _d = _a.raw, raw = _d === void 0 ? false : _d, _e = _a.longKeys, longKeys = _e === void 0 ? false : _e, onClick = _a.onClick;
    if (!utils_1.defined(data) || data.length === 0) {
        return null;
    }
    var getData = function () {
        if (isSorted) {
            return sortBy_1.default(data, [function (_a) {
                    var key = _a.key;
                    return key.toLowerCase();
                }]);
        }
        return data;
    };
    return (<table className="table key-value" onClick={onClick}>
      <tbody>
        {getData().map(function (_a) {
            var key = _a.key, subject = _a.subject, _b = _a.value, value = _b === void 0 ? null : _b, meta = _a.meta, subjectIcon = _a.subjectIcon, subjectDataTestId = _a.subjectDataTestId;
            var dataValue = typeof value === 'object' && !React.isValidElement(value)
                ? JSON.stringify(value, null, 2)
                : value;
            var contentComponent = (<pre className="val-string">
                <annotatedText_1.default value={dataValue} meta={meta}/>
                {subjectIcon}
              </pre>);
            if (isContextData) {
                contentComponent = (<contextData_1.default data={!raw ? value : JSON.stringify(value)} meta={meta} withAnnotatedText>
                  {subjectIcon}
                </contextData_1.default>);
            }
            else if (typeof dataValue !== 'string' && React.isValidElement(dataValue)) {
                contentComponent = dataValue;
            }
            return (<tr key={key}>
                <TableSubject className="key" wide={longKeys}>
                  {subject}
                </TableSubject>
                <td className="val" data-test-id={subjectDataTestId}>
                  {contentComponent}
                </td>
              </tr>);
        })}
      </tbody>
    </table>);
};
var TableSubject = styled_1.default('td')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    max-width: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    max-width: ", ";\n  }\n"])), theme_1.default.breakpoints[2], function (p) { return (p.wide ? '620px !important' : 'none'); });
KeyValueList.displayName = 'KeyValueList';
exports.default = KeyValueList;
var templateObject_1;
//# sourceMappingURL=keyValueList.jsx.map