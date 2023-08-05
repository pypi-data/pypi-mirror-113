Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var clipboardTooltip_1 = tslib_1.__importDefault(require("app/components/clipboardTooltip"));
var tooltip_1 = require("app/components/tooltip");
describe('ClipboardTooltip', function () {
    it('renders', function () {
        var title = 'tooltip content';
        var wrapper = enzyme_1.mountWithTheme(<clipboardTooltip_1.default title={title}>
        <span>This text displays a tooltip when hovering</span>
      </clipboardTooltip_1.default>);
        jest.useFakeTimers();
        var trigger = wrapper.find('span');
        trigger.simulate('mouseEnter');
        jest.advanceTimersByTime(tooltip_1.OPEN_DELAY);
        wrapper.update();
        var tooltipClipboardWrapper = wrapper.find('TooltipClipboardWrapper');
        expect(tooltipClipboardWrapper.length).toEqual(1);
        var tooltipTextContent = tooltipClipboardWrapper.find('TextOverflow');
        expect(tooltipTextContent.length).toEqual(1);
        var clipboardContent = tooltipClipboardWrapper.find('Clipboard');
        expect(clipboardContent.length).toEqual(1);
        expect(clipboardContent.props().value).toEqual(title);
        var iconCopy = clipboardContent.find('IconCopy');
        expect(iconCopy.length).toEqual(1);
    });
});
//# sourceMappingURL=clipboardTooltip.spec.jsx.map