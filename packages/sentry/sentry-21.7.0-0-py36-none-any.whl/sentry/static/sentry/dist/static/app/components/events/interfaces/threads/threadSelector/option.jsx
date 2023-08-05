Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var styles_1 = require("./styles");
var Option = function (_a) {
    var id = _a.id, details = _a.details, name = _a.name, crashed = _a.crashed, crashedInfo = _a.crashedInfo;
    var _b = details.label, label = _b === void 0 ? "<" + locale_1.t('unknown') + ">" : _b, _c = details.filename, filename = _c === void 0 ? "<" + locale_1.t('unknown') + ">" : _c;
    var optionName = name || "<" + locale_1.t('unknown') + ">";
    return (<styles_1.Grid>
      <styles_1.GridCell>
        <InnerCell>
          <tooltip_1.default title={"#" + id} position="top">
            <textOverflow_1.default>{"#" + id}</textOverflow_1.default>
          </tooltip_1.default>
        </InnerCell>
      </styles_1.GridCell>
      <styles_1.GridCell>
        <InnerCell isBold>
          <tooltip_1.default title={optionName} position="top">
            <textOverflow_1.default>{optionName}</textOverflow_1.default>
          </tooltip_1.default>
        </InnerCell>
      </styles_1.GridCell>
      <styles_1.GridCell>
        <InnerCell color="blue300">
          <tooltip_1.default title={label} position="top">
            <textOverflow_1.default>{label}</textOverflow_1.default>
          </tooltip_1.default>
        </InnerCell>
      </styles_1.GridCell>
      <styles_1.GridCell>
        <InnerCell color="purple300">
          <tooltip_1.default title={filename} position="top">
            <textOverflow_1.default>{filename}</textOverflow_1.default>
          </tooltip_1.default>
        </InnerCell>
      </styles_1.GridCell>
      <styles_1.GridCell>
        {crashed && (<InnerCell isCentered>
            {crashedInfo ? (<tooltip_1.default skipWrapper title={locale_1.tct('Errored with [crashedInfo]', {
                    crashedInfo: crashedInfo.values[0].type,
                })} position="top">
                <icons_1.IconFire color="red300"/>
              </tooltip_1.default>) : (<icons_1.IconFire color="red300"/>)}
          </InnerCell>)}
      </styles_1.GridCell>
    </styles_1.Grid>);
};
exports.default = Option;
var InnerCell = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: ", ";\n  font-weight: ", ";\n  ", "\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: ", ";\n  font-weight: ", ";\n  ", "\n"])), function (p) { return (p.isCentered ? 'center' : 'flex-start'); }, function (p) { return (p.isBold ? 600 : 400); }, function (p) { return p.color && "color: " + p.theme[p.color]; });
var templateObject_1;
//# sourceMappingURL=option.jsx.map