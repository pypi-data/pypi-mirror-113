Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var ownerInput_1 = tslib_1.__importDefault(require("app/views/settings/project/projectOwnership/ownerInput"));
var EditOwnershipRulesModal = /** @class */ (function (_super) {
    tslib_1.__extends(EditOwnershipRulesModal, _super);
    function EditOwnershipRulesModal() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EditOwnershipRulesModal.prototype.render = function () {
        var ownership = this.props.ownership;
        return (<react_1.Fragment>
        <Block>
          {locale_1.t('Rules follow the pattern: ')} <code>type:glob owner owner</code>
        </Block>
        <Block>
          {locale_1.t('Owners can be team identifiers starting with #, or user emails')}
        </Block>
        <Block>
          {locale_1.t('Globbing Syntax:')}
          <CodeBlock>{'* matches everything\n? matches any single character'}</CodeBlock>
        </Block>
        <Block>
          {locale_1.t('Examples')}
          <CodeBlock>
            path:src/example/pipeline/* person@sentry.io #infrastructure
            {'\n'}
            url:http://example.com/settings/* #product
            {'\n'}
            tags.sku_class:enterprise #enterprise
          </CodeBlock>
        </Block>
        {ownership && <ownerInput_1.default {...this.props} initialText={ownership.raw || ''}/>}
      </react_1.Fragment>);
    };
    return EditOwnershipRulesModal;
}(react_1.Component));
var Block = styled_1.default(textBlock_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 16px;\n"], ["\n  margin-bottom: 16px;\n"])));
var CodeBlock = styled_1.default('pre')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  word-break: break-all;\n  white-space: pre-wrap;\n"], ["\n  word-break: break-all;\n  white-space: pre-wrap;\n"])));
exports.default = EditOwnershipRulesModal;
var templateObject_1, templateObject_2;
//# sourceMappingURL=editRulesModal.jsx.map