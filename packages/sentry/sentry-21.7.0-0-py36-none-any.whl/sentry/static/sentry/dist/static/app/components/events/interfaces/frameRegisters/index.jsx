Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var utils_2 = require("./utils");
var value_1 = tslib_1.__importDefault(require("./value"));
function FrameRegisters(_a) {
    var registers = _a.registers, deviceArch = _a.deviceArch;
    // make sure that clicking on the registers does not actually do
    // anything on the containing element.
    var handlePreventToggling = function (event) {
        event.stopPropagation();
    };
    var sortedRegisters = utils_2.getSortedRegisters(registers, deviceArch);
    return (<Wrapper>
      <Heading>{locale_1.t('registers')}</Heading>
      <Registers>
        {sortedRegisters.map(function (_a) {
            var _b = tslib_1.__read(_a, 2), name = _b[0], value = _b[1];
            if (!utils_1.defined(value)) {
                return null;
            }
            return (<Register key={name} onClick={handlePreventToggling}>
              <Name>{name}</Name>
              <value_1.default value={value} meta={metaProxy_1.getMeta(registers, name)}/>
            </Register>);
        })}
      </Registers>
    </Wrapper>);
}
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border-top: 1px solid ", ";\n  padding-top: 10px;\n"], ["\n  border-top: 1px solid ", ";\n  padding-top: 10px;\n"])), function (p) { return p.theme.innerBorder; });
var Registers = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  margin-left: 125px;\n  padding: ", " 0px;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  margin-left: 125px;\n  padding: ", " 0px;\n"])), space_1.default(0.25));
var Register = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: ", " 5px;\n"], ["\n  padding: ", " 5px;\n"])), space_1.default(0.5));
var Heading = styled_1.default('strong')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-weight: 600;\n  font-size: 13px;\n  width: 125px;\n  max-width: 125px;\n  word-wrap: break-word;\n  padding: 10px 15px 10px 0;\n  line-height: 1.4;\n  float: left;\n"], ["\n  font-weight: 600;\n  font-size: 13px;\n  width: 125px;\n  max-width: 125px;\n  word-wrap: break-word;\n  padding: 10px 15px 10px 0;\n  line-height: 1.4;\n  float: left;\n"])));
var Name = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  font-size: 13px;\n  font-weight: 600;\n  text-align: right;\n  width: 4em;\n"], ["\n  display: inline-block;\n  font-size: 13px;\n  font-weight: 600;\n  text-align: right;\n  width: 4em;\n"])));
exports.default = FrameRegisters;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map